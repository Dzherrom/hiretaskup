from django.shortcuts import render
from .models import Crud
from django.db import IntegrityError

# Create your views here.

def home(request):
    return render(request, 'home.html', {})

def crud(request):
    list = Crud.objects.all()
    return render(request, 'crud.html', {'list': list})

def register(request):
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')

        if Crud.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'El correo ya está registrado.'})

        try:
            crud = Crud(
                last_name=last_name,
                first_name=first_name,
                email=email,
                phone=phone,
                address=address,
                password=password
            )
            crud.save()
        except IntegrityError:
            return render(request, 'register.html', {'error': 'Error al guardar el registro.'})

    return render(request, 'register.html', {})