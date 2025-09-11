from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import CustomUser, Meeting
from .forms import MeetingForm
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.conf import settings
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
            return redirect('home')  # Redirige a la página principal
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
    return render(request, 'user/user_profile.html', {'user': request.user})

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
    
### CONTACT ###
@login_required
def contact(request):
    if request.method == 'POST':
        print(request.POST)
        form = MeetingForm(request.POST)
        if form.is_valid():
            try:
                form.save()
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