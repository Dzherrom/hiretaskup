from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    # Add any additional fields you want to include in your custom user model
    # For example, you can add a profile picture field
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    full_name = models.CharField(max_length=100, default="No Last Name")
    address = models.TextField(default="No Address")
    business_name = models.CharField(max_length=100, default="No Business Name")
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.first_name
        return self.last_name


class VirtualAssistant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    plan_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    assistants = models.ManyToManyField(VirtualAssistant, blank=True, related_name='subscriptions')

    def __str__(self):
        return f"{self.user.username} - {self.plan_name} ({'active' if self.active else 'inactive'})"
    
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