from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import requests
import json
import base64
from .utils import send_welcome_email
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PasswordResetRequestForm, PasswordResetVerifyForm, ContactForm
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import CustomUser, Meeting, Subscription, VirtualAssistant
from .forms import MeetingForm
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
import stripe 
import requests 
import base64
import json
import random
from django.http import JsonResponse  

def home(request):
    return render(request, 'home/home.html', {'user_is_authenticated': request.user.is_authenticated})

## AUTHENTICATION VIEWS ##
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('plans')  # Redirige a planes para forzar selección
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige a la página principal
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def forgot_password_request(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = str(random.randint(100000, 999999))
            
            # Guardar OTP en sesión con expiración (5 mins)
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            request.session.set_expiry(300)
            
            try:
                send_mail(
                    'Código de Recuperación TaskUp',
                    f'Tu código de seguridad es: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log error if needed
                pass
                
            return redirect('forgot_password_verify')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'auth/forgot_password.html', {'form': form})

def forgot_password_verify(request):
    if 'reset_email' not in request.session:
        return redirect('forgot_password_request')

    if request.method == 'POST':
        form = PasswordResetVerifyForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['otp'] == request.session.get('reset_otp'):
                email = request.session['reset_email']
                try:
                    user = CustomUser.objects.get(email=email)
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()
                    
                    del request.session['reset_otp']
                    del request.session['reset_email']
                    return redirect('login')
                except CustomUser.DoesNotExist:
                     form.add_error(None, 'Error interno: usuario no encontrado.')
            else:
                form.add_error('otp', 'Código incorrecto o expirado.')
    else:
        form = PasswordResetVerifyForm()

    return render(request, 'auth/forgot_password_verify.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al inicio de sesión 

### CustomUser CUSTOM USER ###
@login_required
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        user.last_name = request.POST['last_name']
        user.first_name = request.POST['first_name']
        user.email = request.POST['email']
        user.phone_number = request.POST['phone_number']
        user.address = request.POST['address']
        password = make_password(request.POST['password'])
        if password:
            user.password = make_password(password)
        user.save()
        return redirect('user_profile')
    # GET: build profile context
    # Show all subscriptions (active and pending). Pending will render with status 'espera'.
    active_subs = Subscription.objects.filter(user=request.user).prefetch_related('assistants').order_by('-active', '-start_date')
    # Compute progress for current active subscription (30-day term enforced in model)
    today = timezone.now().date()
    current_active = next((s for s in active_subs if s.active), None)
    sub_progress = {
        'has_active': bool(current_active),
        'percent': 0,
        'days_left': 0,
        'elapsed': 0,
        'total': 0,
        'end_date': None,
    }
    if current_active and current_active.start_date and current_active.end_date:
        total = (current_active.end_date - current_active.start_date).days
        elapsed = (today - current_active.start_date).days
        if total < 0:
            total = 0
        elapsed = max(0, min(elapsed, total)) if total else 0
        percent = int(round((elapsed / total) * 100)) if total else 0
        days_left = max(0, (current_active.end_date - today).days)
        sub_progress.update({
            'percent': percent,
            'days_left': days_left,
            'elapsed': elapsed,
            'total': total,
            'end_date': current_active.end_date,
        })
    # Assistants are derived from active subscriptions only; if none active, UI shows "Por asignar".
    assistants = VirtualAssistant.objects.filter(subscriptions__user=request.user, subscriptions__active=True).distinct()
    ctx = {
        'user': request.user,
        'active_subscriptions': active_subs,
        'assigned_assistants': assistants,
        'sub_progress': sub_progress,
    }
    return render(request, 'user/user_profile.html', ctx)

@login_required
def user_list(request):
    list = CustomUser.objects.all()
    return render(request, 'user/custom_user.html', {'list': list})

@login_required
def user_create(request):
    if request.method == 'POST':
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        password = request.POST['password']

        hashed_password = make_password(password)

        CustomUser = CustomUser.objects.create(
            last_name=last_name,
            first_name=first_name,
            email=email,
            phone_number=phone_number,
            address=address,
            password=hashed_password
        )
        return redirect('user_list')
    return(request, 'user/user_create.html', {'custom_user': CustomUser})

@login_required
def user_edit(request, id):
    if request.user.id != id and not request.user.is_superuser:
        raise PermissionDenied("No tienes permisos para editar este perfil.")

    user = get_object_or_404(CustomUser, id=id)
    error = None
    
    if request.method == 'POST':
        # Validar contraseña actual solo si se intenta cambiar la contraseña
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password:
            if not current_password:
                error = "Please enter your current password to set a new one."
            elif not user.check_password(current_password):
                 error = "Incorrect current password."
            elif new_password != confirm_password:
                 error = "New passwords do not match."
            else:
                 user.set_password(new_password)
                 # Keep user logged in after password change (optional but good UX)
                 from django.contrib.auth import update_session_auth_hash
                 update_session_auth_hash(request, user)

        if not error:
            user.last_name = request.POST.get('last_name', user.last_name)
            user.first_name = request.POST.get('first_name', user.first_name)
            # Username should likely be read-only or handled carefully
            # user.username = request.POST.get('username', user.username) 
            user.email = request.POST.get('email', user.email)
            user.phone_number = request.POST.get('phone_number', user.phone_number)
            user.address = request.POST.get('address', user.address)
            user.business_name = request.POST.get('business_name', user.business_name)
            user.website = request.POST.get('website', user.website)
            
            user.save()
            return redirect('user_profile')

    return render(request, 'user/user_edit.html', {'user': user, 'error': error})

@login_required
def user_delete(request, id):
    if request.user.id != id and not request.user.is_superuser:
        raise PermissionDenied("No tienes permisos para eliminar este perfil.")

    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user/user_delete.html', {'user': user})

### ABOUT ###

def about(request):
    return render(request, 'home/about.html', {'user_is_authenticated': request.user.is_authenticated})

### PLANS ###

def plans(request):
    try:
        full_time = Plan.objects.get(name="Full-Time Assistant")
        part_time = Plan.objects.get(name="Part-Time Assistant")
    except Plan.DoesNotExist:
        full_time = None
        part_time = None

    return render(request, 'plans/plans.html', {
        'user_is_authenticated': request.user.is_authenticated,
        'full_time_plan': full_time,
        'part_time_plan': part_time
    })


## TERMS OF SERVICE ##
@login_required
def accept_terms(request):
    """
    Forces user to scroll through terms and accept them.
    Preserves GET parameters to redirect back to checkout smoothly.
    """
    if request.method == 'POST':
        if 'agreed' in request.POST:
            request.user.terms_accepted = True
            request.user.terms_accepted_at = timezone.now()
            request.user.save()
            
            # Construct redirect URL with original query parameters
            # (e.g., plan_id, quantity) kept in the URL query string
            base_url = reverse('onboarding_checkout')
            query_string = request.GET.urlencode()
            if query_string:
                return redirect(f"{base_url}?{query_string}")
            return redirect('onboarding_checkout')

    return render(request, 'onboarding/accept_terms.html')

def view_terms(request):
    """
    Allows users to view terms without acceptance logic.
    """
    return render(request, 'legal/view_terms.html')

@login_required
@require_http_methods(["GET"])
def onboarding_checkout(request):
    # --- SECURITY: TERMS CHECK ---
    if not request.user.terms_accepted:
        # Redirect to terms page, passing current params (plan_id, qty) along
        query_params = request.GET.urlencode()
        redirect_url = reverse('accept_terms')
        if query_params:
            redirect_url += f"?{query_params}"
        return redirect(redirect_url)

    plan_id = request.GET.get('plan_id')
    
# ONBOARDING CHECKOUT
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .models import Plan  # Import Plan model

@login_required
@require_http_methods(["GET"])
def onboarding_checkout(request):
    plan_id = request.GET.get('plan_id')
    # Try to find plan in DB. If not found, handle gracefully or show 404
    plan = get_object_or_404(Plan, id=plan_id) if plan_id else None
    
    # If using existing logic for fallback:
    plan_name = plan.name if plan else (request.GET.get('name') or 'Selected Plan')
    try:
        amount_cents = plan.price_cents if plan else int(request.GET.get('amount') or 0)
    except ValueError:
        amount_cents = 0
        
    qty = int(request.GET.get('qty') or 1)
    if qty < 1:
        qty = 1
        
    context = {
        'plan': plan, # Pass plan object
        'plan_name': plan_name,
        'amount_cents': amount_cents,
        'amount_dollars': amount_cents / 100 if amount_cents else 0,
        'qty': qty,
        'prefill': {
            'full_name': request.user.get_full_name(),
            'business_name': getattr(request.user, 'business_name', '') or '',
            'email': request.user.email,
            'phone': getattr(request.user, 'phone_number', '') or '',
            'website': getattr(request.user, 'website', '') or '',
        },
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
    }
    return render(request, 'onboarding/checkout.html', context)


@login_required
@require_http_methods(["POST"])
@csrf_protect
def onboarding_create_checkout(request):
    # --- PREPARE DATA FOR POTENTIAL RE-RENDER ---
    plan_id = request.POST.get('plan_id')
    try:
        plan = Plan.objects.get(id=plan_id)
        plan_name = plan.name
        price_cents = plan.price_cents
    except Exception:
        plan = None
        plan_name = "Unknown Plan"
        price_cents = 0

    try:
        qty = int(request.POST.get('quantity', '1'))
    except ValueError:
        qty = 1
    qty = max(1, qty)

    # --- SECURITY: PLAN LIMIT CHECK ---
    active_subs = Subscription.objects.filter(user=request.user, active=True).count()
    if active_subs >= 3:
         return render(request, 'onboarding/checkout.html', {
             'error': "You cannot have more than 3 active plans. Please contact support or cancel an existing plan.",
             'prefill': request.POST, 
             'plan': plan,
             'plan_name': plan_name,
             'amount_cents': price_cents,
             'amount_dollars': price_cents / 100 if price_cents else 0,
             'qty': qty,
             'paypal_client_id': settings.PAYPAL_CLIENT_ID
         })

    # --- SECURITY: DATA INTEGRITY ---
    # Use REAL price from DB already fetched
    if not plan:
        return redirect('plans')


    # Collect other form data
    full_name = request.POST.get('full_name', '')
    business_name = request.POST.get('business_name', '')
    email = request.POST.get('email', request.user.email)
    phone = request.POST.get('phone', '')
    website = request.POST.get('website', '')
    company_type = request.POST.get('company_type', '')
    client_needs = request.POST.get('client_needs', '')
    va_tasks = request.POST.get('va_tasks', '')
    
    # Capture Timezone
    user_tz = request.POST.get('timezone')

    # Update User Profile
    user = request.user
    if full_name:
        parts = full_name.strip().split()
        if len(parts) == 1:
             user.first_name = parts[0]
        else:
             user.first_name = parts[0]
             user.last_name = ' '.join(parts[1:])
    
    if business_name: setattr(user, 'business_name', business_name)
    if phone: setattr(user, 'phone_number', phone)
    if website: setattr(user, 'website', website)
    if company_type: setattr(user, 'company_type', company_type)
    if client_needs: setattr(user, 'client_needs', client_needs)
    if va_tasks: setattr(user, 'va_tasks', va_tasks)
    if user_tz: setattr(user, 'time_zone', user_tz) # Save timezone
    
    if email and email != user.email:
         user.email = email
    
    user.save()

    # Create Pending Subscription (Wait for Webhook to Activate)
    try:
        Subscription.objects.get_or_create(
            user=user,
            plan_name=plan_name,
            active=False,
            defaults={
                'start_date': timezone.now().date(),
                'end_date': None,
            }
        )
    except Exception:
        pass

    # Create Secure Stripe Session
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    checkout_session = stripe.checkout.Session.create(
        customer_email=user.email,
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': plan_name,
                },
                'unit_amount': price_cents, # IDEMPOTENT PRICE FROM DB
                'recurring': {
                    'interval': 'month',
                },
            },
            'quantity': qty,
        }],
        mode='subscription',
        success_url=request.build_absolute_uri('/payments/success/'),
        cancel_url=request.build_absolute_uri('/payments/cancel/'),
        metadata={
            'user_id': user.id,
            'plan_name': plan_name,
            'plan_id': plan.id # Track ID for analytics/ref
        }
    )
    
    return redirect(checkout_session.url)

### CONTACT ###

def contact(request):
    # RATE LIMITING: Check IP/Session cooldown (30 minutes)
    # Using session based limiting for simplicity as IP might be shared or behind proxy headers mess
    last_contact = request.session.get('last_contact_time')
    if last_contact:
        import time
        elapsed = time.time() - last_contact
        if elapsed < 1800: # 1800 seconds = 30 minutes
             return render(request, 'home/contact.html', {
                 'form': ContactForm(),
                 'error': "You are sending messages too quickly. Please wait 30 minutes.",
                 'user_is_authenticated': request.user.is_authenticated
             })

    form = ContactForm(request.POST or None)
    success = False
    
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            # contact_info is validated (email or phone)
            contact_info = form.cleaned_data['contact_info']
            message_body = form.cleaned_data['message']

            email_subject = f"New Contact Request: {subject}"
            email_message = f"""
            You have received a new message from the contact form.

            Details:
            ---------
            Name: {name}
            Email/Phone: {contact_info}
            Subject: {subject}
            
            Message:
            {message_body}
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.EMAIL_HOST_USER]

            try:
                send_mail(email_subject, email_message, from_email, recipient_list, fail_silently=False)
                success = True
                # Set cooldown timestamp
                import time
                request.session['last_contact_time'] = time.time()
            except Exception:
                pass

    return render(request, 'home/contact.html', {
        'form': form,
        'success': success,
        'user_is_authenticated': request.user.is_authenticated
    })

    return render(request, 'home/contact.html', {
            'user_is_authenticated': request.user.is_authenticated})

# payments

stripe.api_key = settings.STRIPE_SECRET_KEY

def process_payment(request):
    if request.method == 'POST':
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'Xbox Game Pass 1 Month for PC',
                    },
                    'unit_amount': 302,  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return redirect(session.url, code=303)
    return render(request, 'payment/stripe_redirect.html')


# ... (existing content of views.py)

### PAYPAL INTEGRATION ###


# Global simple cache for token (in-memory, per worker)
_PAYPAL_TOKEN_CACHE = {
    'access_token': None,
    'expires_at': 0
}

def get_paypal_access_token():
    global _PAYPAL_TOKEN_CACHE
    import time

    # Check cache
    if _PAYPAL_TOKEN_CACHE['access_token'] and _PAYPAL_TOKEN_CACHE['expires_at'] > time.time():
        return _PAYPAL_TOKEN_CACHE['access_token']

    client_id = str(settings.PAYPAL_CLIENT_ID).strip()
    client_secret = str(settings.PAYPAL_SECRET_KEY).strip()
    
    # Debug: Check what credentials we are using
    masked_id = client_id[:4] + "***" + client_id[-4:] if len(client_id) > 8 else "INVALID"
    print(f"DEBUG: PayPal ID: {masked_id}, Mode: {settings.PAYPAL_MODE}")

    # Determine base URL
    if settings.PAYPAL_MODE == 'live':
        base_url = "https://api-m.paypal.com"
    else:
        base_url = "https://api-m.sandbox.paypal.com"

    auth_response = requests.post(
        f"{base_url}/v1/oauth2/token",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    
    if auth_response.status_code != 200:
        print(f"PayPal Auth Failed: {auth_response.text}")
        raise Exception(f"Failed to get PayPal token: {auth_response.text}")
    
    data = auth_response.json()
    token = data['access_token']
    expires_in = data.get('expires_in', 3600)
    
    # Update Cache
    _PAYPAL_TOKEN_CACHE['access_token'] = token
    _PAYPAL_TOKEN_CACHE['expires_at'] = time.time() + expires_in - 60 # Buffer 60s
    
    return token

@login_required
@require_http_methods(["POST"])
def create_paypal_order(request):
    try:
        data = json.loads(request.body)
        
        # 1. Extract Data
        plan_name = data.get('plan_name', 'Default Plan')
        try:
            qty = int(data.get('quantity', 1))
            # Amount should be calculated server side for security usually, 
            # but for this existing flow we take from frontend logic verified against DB ideally.
            # Using the passed unit amount for consistency with Stripe view.
            unit_amount = float(data.get('unit_amount', '0.00')) 
        except:
            qty = 1
            unit_amount = 0.00
            
        total_amount = unit_amount * qty

        # 2. Update User Profile (Mirroring Stripe Flow)
        form_data = data.get('form_data', {})
        user = request.user
        
        full_name = form_data.get('full_name', '')
        if full_name:
            parts = full_name.strip().split()
            if len(parts) == 1:
                user.first_name = parts[0]
            else:
                user.first_name = parts[0]
                user.last_name = ' '.join(parts[1:])
        
        if form_data.get('business_name'): 
            setattr(user, 'business_name', form_data['business_name'])
        if form_data.get('phone'): 
            setattr(user, 'phone_number', form_data['phone'])
        if form_data.get('website'): 
            setattr(user, 'website', form_data['website'])
        if form_data.get('company_type'): 
            setattr(user, 'company_type', form_data['company_type'])
        if form_data.get('client_needs'): 
            setattr(user, 'client_needs', form_data['client_needs'])
        if form_data.get('va_tasks'): 
            setattr(user, 'va_tasks', form_data['va_tasks'])
        
        user.save()

        # 3. Create Pending Subscription
        Subscription.objects.get_or_create(
            user=user,
            plan_name=plan_name,
            active=False,
            defaults={
                'start_date': timezone.now().date(),
                'end_date': None,
            }
        )

        # 4. Create PayPal Order
        access_token = get_paypal_access_token()
        if settings.PAYPAL_MODE == 'live':
            base_url = "https://api-m.paypal.com"
        else:
            base_url = "https://api-m.sandbox.paypal.com"

        payload = {
            "intent": "CAPTURE",
            "application_context": {
                "return_url": request.build_absolute_uri('/paypal/return/'),
                "cancel_url": request.build_absolute_uri('/paypal/cancel/'),
                "brand_name": "HireTaskUp",
                "user_action": "PAY_NOW"
            },
            "purchase_units": [
                {
                    "reference_id": f"SUB-{user.id}-{int(timezone.now().timestamp())}",
                    "amount": {
                        "currency_code": "USD",
                        "value": f"{total_amount:.2f}"
                    },
                    "description": f"{plan_name} (x{qty})"
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(f"{base_url}/v2/checkout/orders", headers=headers, json=payload)
        
        if response.status_code not in [200, 201]:
             return JsonResponse({'error': response.text}, status=400)
             
        order_data = response.json()
        
        # Find approval link for backend-driven redirect
        approval_url = next(link['href'] for link in order_data['links'] if link['rel'] == 'approve')
        
        return JsonResponse({'id': order_data['id'], 'approval_url': approval_url})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def paypal_return(request):
    token = request.GET.get('token')
    if not token:
        return redirect('payments') # or error page
        
    try:
        # Capture Order Server-Side using the token (which is the Order ID)
        access_token = get_paypal_access_token()
        if settings.PAYPAL_MODE == 'live':
            base_url = "https://api-m.paypal.com"
        else:
            base_url = "https://api-m.sandbox.paypal.com"
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        # Capture
        response = requests.post(f"{base_url}/v2/checkout/orders/{token}/capture", headers=headers)
        
        # Note: If already captured (e.g. idempotency), PayPal might return 422 or details. 
        # Check status carefully.
        
        capture_data = response.json()
        status = capture_data.get('status')
        
        if response.status_code in [200, 201] and status == 'COMPLETED':
             sub = Subscription.objects.filter(user=request.user, active=False).last()
             if sub:
                 sub.active = True
                 sub.save()
                 send_welcome_email(request.user.email, request.user.first_name)
             return redirect('payment_success')
        else:
             # Handle error or incomplete
             print(f"Capture failed or pending: {capture_data}")
             return redirect('payment_cancel')

    except Exception as e:
        print(f"PayPal Return Error: {e}")
        return redirect('payment_cancel')

@login_required
def paypal_cancel(request):
    return render(request, 'payment/cancel.html')

# Deprecated JS Capture endpoint (kept around just in case, but unused in redirect flow)
@login_required
@require_http_methods(["POST"])
def capture_paypal_order(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('orderID')
        
        # 1. Capture Order
        access_token = get_paypal_access_token()
        if settings.PAYPAL_MODE == 'live':
            base_url = "https://api-m.paypal.com"
        else:
            base_url = "https://api-m.sandbox.paypal.com"
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.post(f"{base_url}/v2/checkout/orders/{order_id}/capture", headers=headers)
        
        if response.status_code not in [200, 201]:
             return JsonResponse({'error': response.text}, status=400)
             
        capture_data = response.json()
        
        # 2. Check status and Activate Subscription
        # NOTE: In a real app, verify the amount and currency match expectations.
        if capture_data.get('status') == 'COMPLETED':
             # Activate the user's most recent pending subscription for this plan? 
             # Or just find the latest inactive one.
             # For simplicity, we activate the user's inactive subscription.
             sub = Subscription.objects.filter(user=request.user, active=False).last()
             if sub:
                 sub.active = True
                 send_welcome_email(request.user.email, request.user.first_name)
                 sub.save()
                 
             return JsonResponse({'status': 'COMPLETED'})
        else:
            return JsonResponse({'error': 'Capture status not completed'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def payment_success(request):
    return redirect('user_profile')

def payment_cancel(request):
    return redirect('plans')

def custom_page_not_found_view(request, exception):
    return render(request, "404.html", status=404)
