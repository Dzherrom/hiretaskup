from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('crud/', views.crud, name='crud'),
    path('register/', views.register),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('update/', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
]