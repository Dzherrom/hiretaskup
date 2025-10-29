from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
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
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": currency,
                "product_data": {"name": product_name},
                "unit_amount": int(price),
            },
            "quantity": 1,
        }],
        success_url=request.build_absolute_uri("/payments/success/"),
        cancel_url=request.build_absolute_uri("/payments/cancel/"),
    )
    return JsonResponse({"id": session.id, "url": session.url})


def payment_success(request):
    return render(request, "payment/success.html")


def payment_cancel(request):
    return render(request, "payment/cancel.html")


@csrf_exempt
def stripe_webhook(request):
    # Verify webhook signature if provided
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        if webhook_secret:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        else:
            event = json.loads(payload)
    except Exception as e:
        return HttpResponse(status=400)

    # Handle event types
    if event.get("type") in ("checkout.session.completed", "payment_intent.succeeded"):
        # You can mark an order as paid here
        pass

    return HttpResponse(status=200)
