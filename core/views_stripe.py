from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Subscription, CustomUser
from .utils import send_invoice_email, send_welcome_email # Import email utility
import stripe
import json


def stripe_config(request):
    return JsonResponse({
        "publicKey": settings.STRIPE_PUBLISHABLE_KEY,
    })


@csrf_exempt
@require_POST
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    data = json.loads(request.body or b"{}")
    price = data.get("amount", 500)  # cents
    currency = data.get("currency", "usd")
    product_name = data.get("name", "Test Product")

    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": currency,
                "product_data": {"name": product_name},
                "unit_amount": int(price),
                "recurring": {"interval": "month"},
            },
            "quantity": 1,
        }],
        success_url=request.build_absolute_uri("/payments/success/"),
        cancel_url=request.build_absolute_uri("/payments/cancel/"),
    )
    return JsonResponse({"id": session.id, "url": session.url})


def payment_success(request):
    return redirect('user_profile')


def payment_cancel(request):
    return redirect('plans')


@csrf_exempt
@require_POST
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # TODO: Obtener el client_reference_id o email, buscar al usuario y activar su suscripción inicial
        
    elif event['type'] == 'invoice.paid':
        invoice = event['data']['object']
        # TODO: Extender la fecha de validez de la suscripción del usuario
        
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        # TODO: Notificar al usuario o marcar su cuenta como "pago pendiente"
        
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        # TODO: Actualizar base de datos si hubo cambio de plan o cancelación programada
        
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # TODO: Revocar acceso premium inmediatamente
        
    else:
        print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200)
