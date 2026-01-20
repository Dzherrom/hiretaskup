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
def stripe_webhook(request):
    # Verify webhook signature if provided
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        # Standard signature verification works for both formats if the secret is correct.
        # However, if using "Thin Events" (Format 2) without signature verification
        # or if the signature fails unexpectedly, we might fall back or log it.
        if webhook_secret and sig_header:
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, webhook_secret
                )
            except ValueError:
                return HttpResponse("Invalid payload", status=400)
            except stripe.error.SignatureVerificationError:
                return HttpResponse("Invalid signature", status=400)
        else:
            # Fallback for testing without validation/headers
            event = json.loads(payload)
    except Exception as e:
        return HttpResponse(status=400)

    # --- HANDLING DUAL FORMATS ---

    # FORMAT 1: Classic ("object": "event")
    if event.get("object") == "event":
        event_type = event.get("type")
        
        if event_type == "checkout.session.completed":
            session = event.get("data", {}).get("object", {})
            metadata = session.get("metadata", {}) or {}
            user_id = metadata.get("user_id")
            plan_name = metadata.get("plan_name", "Selected Plan")
            
            if user_id:
                try:
                    user = CustomUser.objects.get(id=int(user_id))
                except Exception:
                    pass # User not found, ignore
                else:
                    # Logic to activate subscription
                    # 1. Try to find the pending subscription created in checkout view
                    # 2. If not found, create one
                    
                    sub = Subscription.objects.filter(
                        user=user, 
                        plan_name=plan_name, 
                        active=False
                    ).first()
                    
                    if not sub:
                        # Fallback: Create new active subscription
                        sub = Subscription.objects.create(
                            user=user,
                            plan_name=plan_name,
                            active=True,
                            start_date=timezone.now().date()
                        )
                    else:
                        # Activate existing pending subscription
                        sub.active = True
                        sub.start_date = timezone.now().date()
                        sub.save()
                    
                    # --- POST-SALE: SEND INVOICE EMAIL & WELCOME EMAIL ---
                    try:
                        amount_cents = session.get('amount_total', 0)
                        send_invoice_email(user, sub, plan_name, amount_cents)
                        send_welcome_email(user.email, user.first_name)
                    except Exception as e:
                        print(f"Failed to send email: {e}")

        elif event_type == "setup_intent.created":
            # Example logic for setup_intent (from your Format 1 example)
            # setup_intent = event.get("data", {}).get("object", {})
            pass 

    # FORMAT 2: V2 / Thin Events ("object": "v2.core.event")
    elif event.get("object") == "v2.core.event":
        event_type = event.get("type")
        
        # Example logic: v1.billing.meter.error_report_triggered
        if event_type == "v1.billing.meter.error_report_triggered":
            related_object = event.get("related_object", {})
            meter_id = related_object.get("id")
            # Log error or notify admin about meter issue
            print(f"Meter Error Triggered for ID: {meter_id}")
            
        # Add other V2 handlers here...

    return HttpResponse(status=200)
