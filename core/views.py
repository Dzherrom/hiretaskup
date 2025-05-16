from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Crud
from django.http import Http404
from django.contrib.auth.hashers import make_password

# Create your views here.

def home(request):
    return render(request, 'home/home.html', {'user_is_authenticated': request.user.is_authenticated})

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

def crud(request):
    list = Crud.objects.all()
    return render(request, 'crud.html', {'list': list})

def register(request):
    last_name = request.POST['last_name']
    first_name = request.POST['first_name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    password = request.POST['password']

    hashed_password = make_password(password)

    crud = Crud.objects.create(
        last_name=last_name,
        first_name=first_name,
        email=email,
        phone=phone,
        address=address,
        password=hashed_password
    )
    return redirect('/crud/')

def edit(request, id):
    crud = Crud.objects.get(id=id)
    return render(request, 'edit.html', {'crud': crud})

def update(request):
    id = request.POST['id']
    last_name = request.POST['last_name']
    first_name = request.POST['first_name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    password = request.POST['password']

    crud = Crud.objects.get(id=id)
    crud.last_name = last_name
    crud.first_name = first_name
    crud.email = email
    crud.phone = phone
    crud.address = address
    crud.password = make_password(password)
    crud.save()

    return redirect('/crud/')

def delete(request, id):
    try:    
        crud = Crud.objects.get(id=id)
        crud.delete()
    except Crud.DoesNotExist:
        raise Http404("Object not found")
    
    return redirect('/crud/')
