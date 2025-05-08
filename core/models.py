from django.db import models

# Create your models here.

class Crud(models.Model):
    last_name = models.CharField(max_length=100, default="No Last Name")
    first_name = models.CharField(max_length=100, default="No First Name")
    email = models.EmailField(unique=True, default="No Email")
    phone = models.CharField(max_length=9, unique=True, default="No Phone")
    address = models.TextField(default="No Address")
    password = models.CharField(max_length=128, default="No Password")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"