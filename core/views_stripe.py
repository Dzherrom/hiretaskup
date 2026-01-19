from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Subscription, CustomUser
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
    if event.get("type") == "checkout.session.completed":
        session = event.get("data", {}).get("object", {})
        metadata = session.get("metadata", {}) or {}
        user_id = metadata.get("user_id")
        plan_name = metadata.get("plan_name", "Selected Plan")
        # Create a pending subscription (active=False) so UI shows "En espera"
        if user_id:
            try:
                user = CustomUser.objects.get(id=int(user_id))
            except Exception:
                return HttpResponse(status=200)
            # Avoid duplicates on webhook retries by using get_or_create on user/plan_name/active=False
            sub, created = Subscription.objects.get_or_create(
                user=user,
                plan_name=plan_name,
                active=False,
                defaults={
                    'start_date': timezone.now().date(),
                    'end_date': None,
                }
            )
            # If it already existed but has no start_date, ensure it's set
            if not created and not sub.start_date:
                sub.start_date = timezone.now().date()
                sub.save()
    return HttpResponse(status=200)
