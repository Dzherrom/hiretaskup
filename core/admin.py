from django.contrib import admin
from .models import Crud

# Register your models here.

class CrudAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/admin_custom.js',)

admin.site.register(Crud)