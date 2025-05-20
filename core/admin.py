from django.contrib import admin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/admin_custom.js',)    

admin.site.register(CustomUser, CustomUserAdmin)