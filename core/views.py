from django.shortcuts import render, redirect
from .models import Crud

# Create your views here.

def home(request):
    return render(request, 'home.html', {})

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

    crud = Crud.objects.create(
        last_name=last_name,
        first_name=first_name,
        email=email,
        phone=phone,
        address=address,
        password=password
    )
    return redirect('/crud/')

def delete(request, email):
    crud = Crud.objects.get(email=email)
    crud.delete()
    return redirect('/crud/')