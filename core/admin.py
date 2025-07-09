from django.contrib import admin
from .models import CustomUser, Meeting

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