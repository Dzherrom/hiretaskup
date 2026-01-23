from django.urls import path, include
from . import views
from . import views_stripe

urlpatterns = [
    #general urls
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('plans/', views.plans, name='plans'),
    path('legal/accept-terms/', views.accept_terms, name='accept_terms'),
    path('legal/terms/', views.view_terms, name='view_terms'),
    path('onboarding/checkout/', views.onboarding_checkout, name='onboarding_checkout'),
    path('onboarding/create-checkout/', views.onboarding_create_checkout, name='onboarding_create_checkout'),
    path('paypal/create-order/', views.create_paypal_order, name='create_paypal_order'),
    path('paypal/capture-order/', views.capture_paypal_order, name='capture_paypal_order'),
    path('paypal/return/', views.paypal_return, name='paypal_return'),
    path('paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),
    path('contact/', views.contact, name='contact'),
    path('payments/success/', views.payment_success, name='payment_success'),
    path('payments/cancel/', views.payment_cancel, name='payment_cancel'),
    
    # Auth OTP Flows
    path('forgot-password/', views.forgot_password_request, name='forgot_password_request'),
    path('forgot-password/verify/', views.forgot_password_verify, name='forgot_password_verify'),

    #auth urls
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/profile/', views.user_profile, name='user_profile'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/edit/<int:id>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:id>/', views.user_delete, name='user_delete'),
    
    # Stripe Webhook
    path('webhook/', views_stripe.stripe_webhook, name='stripe_webhook'),
]