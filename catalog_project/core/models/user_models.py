# core/models/user_models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .company_models import Company
from core.validators.user_validators import validate_password
from .managers import CustomUserManager
from .base_model import BaseModel

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    # Campos do usuário
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=30, validators=[validate_password])
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    # Campos obrigatórios para AbstractBaseUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'status']

    objects = CustomUserManager()  # Use CustomUserManager

    # Definindo related_name exclusivos para evitar conflitos
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
