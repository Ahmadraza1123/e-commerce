from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('vendor', 'vendor'),
        ('customer', 'customer'),
        ('delivery_boy', 'delivery_boy'),
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    user_profile = models.ImageField(upload_to='profile_pics/', blank=False, null=False)
    address = models.TextField(blank=True, null=True)
    reset_code = models.CharField(max_length=255, blank=True, null=True)





