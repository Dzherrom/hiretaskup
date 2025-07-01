from django.urls import path, include
from . import views

urlpatterns = [
    #general urls
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('plans/', views.plans, name='plans'),
    path('contact/', views.contact, name='contact'),
    #auth urls
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/profile/', views.user_profile, name='user_profile'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/edit/<int:id>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:id>/', views.user_delete, name='user_delete'),
]