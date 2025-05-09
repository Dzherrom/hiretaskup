from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crud/', views.crud, name='crud'),
    path('register/', views.register),
    path('delete/<email>', views.delete),
]