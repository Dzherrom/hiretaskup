from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crud/', views.crud, name='crud'),
    path('register/', views.register),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('update/', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
]