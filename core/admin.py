from django.contrib import admin
from .models import CustomUser, Meeting, Subscription, VirtualAssistant

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/admin_custom.js',)    

admin.site.register(CustomUser, CustomUserAdmin)

class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'guests', 'important', 'phone', 'date', 'time', 'timezone')
    search_fields = ('name', 'email')
    list_filter = ('date', 'time')

    class Media:
        js = ('js/admin_meeting.js',)

admin.site.register(Meeting, MeetingAdmin)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_name', 'start_date', 'end_date', 'active')
    list_filter = ('active', 'start_date')
    search_fields = ('user__username', 'plan_name')

@admin.register(VirtualAssistant)
class VirtualAssistantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')