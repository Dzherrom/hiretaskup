from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class CustomUser(AbstractUser):
    # Add any additional fields you want to include in your custom user model
    # For example, you can add a profile picture field
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    full_name = models.CharField(max_length=100, default="No Last Name")
    address = models.TextField(default="No Address")
    business_name = models.CharField(max_length=100, default="No Business Name")
    website = models.URLField(blank=True, null=True)
    
    # New onboarding fields
    client_needs = models.TextField(blank=True, null=True, help_text="What are your main needs?")
    company_type = models.CharField(max_length=100, blank=True, null=True, help_text="Type of company/industry")
    va_tasks = models.TextField(blank=True, null=True, help_text="Tasks you want the VA to perform")
    time_zone = models.CharField(max_length=100, blank=True, null=True, help_text="Preferred Time Zone")
    
    def __str__(self):
        return self.first_name
        return self.last_name


class VirtualAssistant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

#damn
class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    plan_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    assistants = models.ManyToManyField(VirtualAssistant, blank=True, related_name='subscriptions')

    def __str__(self):
        return f"{self.user.username} - {self.plan_name} ({'active' if self.active else 'inactive'})"
    
    def save(self, *args, **kwargs):
        # Always enforce a 30-day term counted from activation time
        if self.active:
            today = timezone.now().date()
            if self.pk:
                try:
                    original = Subscription.objects.only('active', 'start_date').get(pk=self.pk)
                except Subscription.DoesNotExist:
                    original = None
                # If transitioning from inactive to active, reset start_date to today
                if original and not original.active:
                    self.start_date = today
                elif not self.start_date:
                    self.start_date = today
            else:
                # New active subscription: start now unless explicitly provided
                if not self.start_date:
                    self.start_date = today
            self.end_date = self.start_date + timedelta(days=30)
        else:
            # Pending/inactive subscriptions don't have a fixed end date
            self.end_date = None
        super().save(*args, **kwargs)
    
class Meeting(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    guests = models.TextField(blank=True, null=True)
    important = models.TextField()
    phone = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    timezone = models.CharField(max_length=50, default="UTC")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('name', 'email', 'date', 'time')
        
    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"