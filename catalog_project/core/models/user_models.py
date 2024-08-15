from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .company_models import Company
from .managers import CustomUserManager
from .base_model import BaseModel

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    PROFILE_CHOICES = [
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users', null=False, blank=False)
    is_active = models.BooleanField(default=True)
    profile = models.CharField(max_length=10, choices=PROFILE_CHOICES, default='manager')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'status']

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_permissions_set',
        blank=True
    )
