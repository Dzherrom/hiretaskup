from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html', {})

def crud(request):
    return render(request, 'crud.html', {})