from django.shortcuts import render
from .models import Crud

# Create your views here.

def home(request):
    return render(request, 'home.html', {})

def crud(request):
    list = Crud.objects.all()
    return render(request, 'crud.html', {'list': list})