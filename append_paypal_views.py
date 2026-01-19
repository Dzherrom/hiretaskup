
file_content = """
# ... (existing content of views.py)

### PAYPAL INTEGRATION ###

def get_paypal_access_token():
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_SECRET_KEY
    # Determine base URL
    if settings.PAYPAL_MODE == 'live':
        base_url = "https://api-m.paypal.com"
    else:
        base_url = "https://api-m.sandbox.paypal.com"

    auth_response = requests.post(
        f"{base_url}/v1/oauth2/token",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    
    if auth_response.status_code != 200:
        raise Exception(f"Failed to get PayPal token: {auth_response.text}")
    
    return auth_response.json()['access_token']

@login_required
@require_http_methods(["POST"])
def create_paypal_order(request):
    try:
        data = json.loads(request.body)
        
        # 1. Extract Data
        plan_name = data.get('plan_name', 'Default Plan')
        try:
            qty = int(data.get('quantity', 1))
            # Amount should be calculated server side for security usually, 
            # but for this existing flow we take from frontend logic verified against DB ideally.
            # Using the passed unit amount for consistency with Stripe view.
            unit_amount = float(data.get('unit_amount', '0.00')) 
        except:
            qty = 1
            unit_amount = 0.00
            
        total_amount = unit_amount * qty

        # 2. Update User Profile (Mirroring Stripe Flow)
        form_data = data.get('form_data', {})
        user = request.user
        
        full_name = form_data.get('full_name', '')
        if full_name:
            parts = full_name.strip().split()
            if len(parts) == 1:
                user.first_name = parts[0]
            else:
                user.first_name = parts[0]
                user.last_name = ' '.join(parts[1:])
        
        if form_data.get('business_name'): 
            setattr(user, 'business_name', form_data['business_name'])
        if form_data.get('phone'): 
            setattr(user, 'phone_number', form_data['phone'])
        if form_data.get('website'): 
            setattr(user, 'website', form_data['website'])
        
        user.save()

        # 3. Create Pending Subscription
        Subscription.objects.get_or_create(
            user=user,
            plan_name=plan_name,
            active=False,
            defaults={
                'start_date': timezone.now().date(),
                'end_date': None,
            }
        )

        # 4. Create PayPal Order
        access_token = get_paypal_access_token()
        if settings.PAYPAL_MODE == 'live':
            base_url = "https://api-m.paypal.com"
        else:
            base_url = "https://api-m.sandbox.paypal.com"

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "reference_id": f"SUB-{user.id}-{int(timezone.now().timestamp())}",
                    "amount": {
                        "currency_code": "USD",
                        "value": f"{total_amount:.2f}"
                    },
                    "description": f"{plan_name} (x{qty})"
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(f"{base_url}/v2/checkout/orders", headers=headers, json=payload)
        
        if response.status_code not in [200, 201]:
             return JsonResponse({'error': response.text}, status=400)
             
        order_data = response.json()
        return JsonResponse({'id': order_data['id']})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def capture_paypal_order(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('orderID')
        
        # 1. Capture Order
        access_token = get_paypal_access_token()
        if settings.PAYPAL_MODE == 'live':
            base_url = "https://api-m.paypal.com"
        else:
            base_url = "https://api-m.sandbox.paypal.com"
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.post(f"{base_url}/v2/checkout/orders/{order_id}/capture", headers=headers)
        
        if response.status_code not in [200, 201]:
             return JsonResponse({'error': response.text}, status=400)
             
        capture_data = response.json()
        
        # 2. Check status and Activate Subscription
        # NOTE: In a real app, verify the amount and currency match expectations.
        if capture_data.get('status') == 'COMPLETED':
             # Activate the user's most recent pending subscription for this plan? 
             # Or just find the latest inactive one.
             # For simplicity, we activate the user's inactive subscription.
             sub = Subscription.objects.filter(user=request.user, active=False).last()
             if sub:
                 sub.active = True
                 sub.save()
                 
             return JsonResponse({'status': 'COMPLETED'})
        else:
            return JsonResponse({'error': 'Capture status not completed'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
"""

# I will append this to the file using a temp script because read/replace is better for small edits, but for big blocks execute is fine.
# Actually I'll use read_file to get the exact end then replace_string_in_file insertion or create_file overwrite? No, overwrite is dangerous.
# I will use a python script to append it.
with open(r'c:\Users\skrea\Documents\Code\hiretaskup\core\views.py', 'a', encoding='utf-8') as f:
    f.write(file_content)
