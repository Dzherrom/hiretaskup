import os

path = r"c:\Users\skrea\Documents\Code\hiretaskup\core\views.py"

# 1. Update onboarding_create_checkout
# Add retrieval
old_retrieve = r"""    company_type = request.POST.get('company_type', '')
    client_needs = request.POST.get('client_needs', '')"""

new_retrieve = r"""    company_type = request.POST.get('company_type', '')
    time_zone = request.POST.get('time_zone', '')
    client_needs = request.POST.get('client_needs', '')"""

# Add saving
old_save = r"""    if company_type:
        setattr(user, 'company_type', company_type)
    if client_needs:"""

new_save = r"""    if company_type:
        setattr(user, 'company_type', company_type)
    if time_zone:
        setattr(user, 'time_zone', time_zone)
    if client_needs:"""

# 2. Update create_paypal_order
# Add saving from JSON
old_paypal = r"""        if form_data.get('company_type'): 
            setattr(user, 'company_type', form_data['company_type'])
        if form_data.get('client_needs'):"""

new_paypal = r"""        if form_data.get('company_type'): 
            setattr(user, 'company_type', form_data['company_type'])
        if form_data.get('time_zone'): 
            setattr(user, 'time_zone', form_data['time_zone'])
        if form_data.get('client_needs'):"""

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(old_retrieve, new_retrieve)
content = content.replace(old_save, new_save)
content = content.replace(old_paypal, new_paypal)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("views.py updated")
