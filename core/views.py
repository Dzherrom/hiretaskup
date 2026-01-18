from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
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
import stripe 

def home(request):
    return render(request, 'home/home.html', {'user_is_authenticated': request.user.is_authenticated})

## AUTHENTICATION VIEWS ##
def register_view(request):
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
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige a la página principal
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

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
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        user.last_name = request.POST['last_name']
        user.first_name = request.POST['first_name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.phone_number = request.POST['phone_number']
        user.address = request.POST['address']
        new_password = request.POST['password']
        if new_password:
            user.password = make_password(new_password)
        user.save()
        return redirect('user_profile')
    return render(request, 'user/user_edit.html', {'user': user})

@login_required
def user_delete(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user/user_delete.html', {'user': user})

### ABOUT ###
@login_required
def about(request):
    return render(request, 'home/about.html', {'user_is_authenticated': request.user.is_authenticated})

### PLANS ###
@login_required
def plans(request):
    return render(request, 'plans/plans.html', {'user_is_authenticated': request.user.is_authenticated})
    
# ONBOARDING CHECKOUT
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

@login_required
@require_http_methods(["GET"])
def onboarding_checkout(request):
    plan_name = request.GET.get('name') or 'Selected Plan'
    try:
        amount_cents = int(request.GET.get('amount') or 0)
    except ValueError:
        amount_cents = 0
    qty = int(request.GET.get('qty') or 1)
    if qty < 1:
        qty = 1
    context = {
        'plan_name': plan_name,
        'amount_cents': amount_cents,
        'amount_dollars': amount_cents / 100 if amount_cents else 0,
        'qty': qty,
        # Prefill form from user data where possible
        'prefill': {
            'full_name': request.user.get_full_name() if hasattr(request.user, 'get_full_name') else '',
            'business_name': getattr(request.user, 'business_name', '') or '',
            'email': request.user.email,
            'phone': getattr(request.user, 'phone_number', '') or '',
            'website': getattr(request.user, 'website', '') or '',
        }
    }
    return render(request, 'onboarding/checkout.html', context)


@login_required
@require_http_methods(["POST"])
@csrf_protect
def onboarding_create_checkout(request):
    # Collect form data
    plan_name = request.POST.get('plan_name', 'Selected Plan')
    try:
        amount_cents = int(request.POST.get('amount_cents', '0'))
        qty = int(request.POST.get('quantity', '1'))
    except ValueError:
        amount_cents, qty = 0, 1
    qty = max(1, qty)

    full_name = request.POST.get('full_name', '')
    business_name = request.POST.get('business_name', '')
    email = request.POST.get('email', request.user.email)
    phone = request.POST.get('phone', '')
    website = request.POST.get('website', '')

    # Update the logged-in user's profile with submitted info
    user = request.user
    # Split full_name into first/last if possible
    if full_name:
        parts = full_name.strip().split()
        if len(parts) == 1:
            user.first_name = parts[0]
        else:
            user.first_name = parts[0]
            user.last_name = ' '.join(parts[1:])
    if business_name:
        setattr(user, 'business_name', business_name)
    if phone:
        setattr(user, 'phone_number', phone)
    if website:
        setattr(user, 'website', website)
    if email and email != user.email:
        user.email = email
    # Optionally set a composite full_name field if present in model
    if hasattr(user, 'full_name') and full_name:
        setattr(user, 'full_name', full_name)
    user.save()

    # Ensure a pending subscription exists so the profile shows "espera" immediately
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
        # Non-fatal: if something goes wrong, still proceed to Stripe
        pass

    # Create Stripe Checkout Session
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        mode='payment',
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': plan_name},
                'unit_amount': amount_cents,
            },
            'quantity': qty,
        }],
        customer_email=email or None,
        success_url=request.build_absolute_uri('/payments/success/'),
        cancel_url=request.build_absolute_uri('/payments/cancel/'),
        metadata={
            'user_id': str(request.user.id),
            'full_name': full_name,
            'business_name': business_name,
            'phone': phone,
            'website': website,
            'plan_name': plan_name,
            'qty': str(qty),
            'amount_cents': str(amount_cents),
        }
    )
    return redirect(session.url, code=303)
### CONTACT ###
@login_required
def contact(request):
    if request.method == 'POST':
        print(request.POST)
        form = MeetingForm(request.POST)
        if form.is_valid():
            try:
                meeting = form.save()

                # --- START EMAIL SENDING LOGIC ---
                subject = f"New Meeting Request: {meeting.name}"
                message = f"""
                You have received a new meeting request.

                Details:
                Name: {meeting.name}
                Email: {meeting.email}
                Phone: {meeting.phone}
                Date: {meeting.date}
                Time: {meeting.time}
                Timezone: {meeting.timezone}
                Guests: {meeting.guests}
                Important Info: {meeting.important}
                """
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [settings.EMAIL_HOST_USER]  # Send to the admin/configured email

                try:
                    send_mail(subject, message, from_email, recipient_list)
                    print("Email sent successfully.")
                except Exception as e:
                    print(f"Error sending email: {e}")
                # --- END EMAIL SENDING LOGIC ---

                return render(request, 'home/contact.html', {
                    'form': MeetingForm(),
                    'success': True, 
                    'user_is_authenticated': request.user.is_authenticated
                })
            except IntegrityError:
                form.add_error(None, "This meeting already exists.")

    else:
        form = MeetingForm()
        return render(request, 'home/contact.html', {
            'form': form,
            'user_is_authenticated': request.user.is_authenticated})
    return render(request, 'home/contact.html', {
            'form': form,
            'error': "This meeting already exists",
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

def payments_page(request):
    return render(request, 'payment/payments.html')