from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    # Add any additional fields you want to include in your custom user model
    # For example, you can add a profile picture field
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Crud(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100, default="No Last Name")
    first_name = models.CharField(max_length=100, default="No First Name")
    email = models.EmailField(unique=True, default="No Email")
    phone = models.CharField(max_length=10, unique=True, default="No Phone")
    address = models.TextField(default="No Address")
    password = models.CharField(max_length=128, default="No Password")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"