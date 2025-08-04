from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    # Add any additional fields you want to include in your custom user model
    # For example, you can add a profile picture field
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=100, default="No Last Name")
    first_name = models.CharField(max_length=100, default="No First Name")
    address = models.TextField(default="No Address")
    
    def __str__(self):
        return self.first_name
        return self.last_name
    
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