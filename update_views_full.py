import os

path = r"c:\Users\skrea\Documents\Code\hiretaskup\core\views.py"

# 1. Update onboarding_create_checkout (Save fields + Stripe Subscription)
old_post_block = r"""    phone = request.POST.get('phone', '')
    website = request.POST.get('website', '')

    # Update the logged-in user's profile with submitted info"""

new_post_block = r"""    phone = request.POST.get('phone', '')
    website = request.POST.get('website', '')
    company_type = request.POST.get('company_type', '')
    client_needs = request.POST.get('client_needs', '')
    va_tasks = request.POST.get('va_tasks', '')

    # Update the logged-in user's profile with submitted info"""

old_save_block = r"""    if website:
        setattr(user, 'website', website)
    if email and email != user.email:"""

new_save_block = r"""    if website:
        setattr(user, 'website', website)
    if company_type:
        setattr(user, 'company_type', company_type)
    if client_needs:
        setattr(user, 'client_needs', client_needs)
    if va_tasks:
        setattr(user, 'va_tasks', va_tasks)
    if email and email != user.email:"""

old_stripe_block = r"""    session = stripe.checkout.Session.create(
        mode='payment',
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': plan_name},
                'unit_amount': amount_cents,
            },
            'quantity': qty,
        }],"""

new_stripe_block = r"""    session = stripe.checkout.Session.create(
        mode='subscription',
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': plan_name},
                'unit_amount': amount_cents,
                'recurring': {'interval': 'month'},
            },
            'quantity': qty,
        }],"""

# 2. Update create_paypal_order (Save fields - JSON)
old_paypal_block = r"""        if form_data.get('website'): 
            setattr(user, 'website', form_data['website'])
        
        user.save()"""

new_paypal_block = r"""        if form_data.get('website'): 
            setattr(user, 'website', form_data['website'])
        if form_data.get('company_type'): 
            setattr(user, 'company_type', form_data['company_type'])
        if form_data.get('client_needs'): 
            setattr(user, 'client_needs', form_data['client_needs'])
        if form_data.get('va_tasks'): 
            setattr(user, 'va_tasks', form_data['va_tasks'])
        
        user.save()"""

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Apply replacements
if old_post_block in content:
    content = content.replace(old_post_block, new_post_block)
else:
    print("Post block match failed")

if old_save_block in content:
    content = content.replace(old_save_block, new_save_block)
else:
    print("Save block match failed")

if old_stripe_block in content:
    content = content.replace(old_stripe_block, new_stripe_block)
else:
    print("Stripe block match failed")

if old_paypal_block in content:
    content = content.replace(old_paypal_block, new_paypal_block)
else:
    print("Paypal block match failed")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("views.py updated.")
