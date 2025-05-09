from django.shortcuts import render, redirect
from .models import Crud
from django.http import Http404

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
    crud.password = password
    crud.save()

    return redirect('/crud/')

def delete(request, id):
    try:    
        crud = Crud.objects.get(id=id)
        crud.delete()
    except Crud.DoesNotExist:
        raise Http404("Object not found")
    
    return redirect('/crud/')
