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
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True, default="https://example.com")
    
    def __str__(self):
        return self.first_name
        return self.last_name