import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hiretaskup.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS core_plan CASCADE")
    print("Table core_plan dropped.")
