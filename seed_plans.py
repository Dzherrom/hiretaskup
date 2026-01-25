import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hiretaskup.settings')
django.setup()
from core.models import Plan

# Create Part-Time Plan
pt, created = Plan.objects.get_or_create(
    name="Part-Time Assistant",
    defaults={
        'price_cents': 79900,
        'description': "20 hrs/week dedicated assistant"
    }
)
if not created and pt.price_cents != 79900:
    pt.price_cents = 79900
    pt.save()
print(f"Plan {pt.name} ID: {pt.id}")

# Create Full-Time Plan
ft, created = Plan.objects.get_or_create(
    name="Full-Time Assistant",
    defaults={
        'price_cents': 149900,
        'description': "40 hrs/week dedicated assistant"
    }
)
if not created and ft.price_cents != 149900:
    ft.price_cents = 149900
    ft.save()
print(f"Plan {ft.name} ID: {ft.id}")
