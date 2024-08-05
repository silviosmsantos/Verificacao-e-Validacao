from django.db import models
from django.core.validators import EmailValidator
from .base_model import BaseModel
from .company_models import Company
from core.validators.user_validators import validate_password

class User(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator("Enter a valid email address.")],
        blank=False,
        null=False
    )
    phone = models.CharField(max_length=20, null=False, blank=False)
    password = models.CharField(
        max_length=30,
        validators=[validate_password],
        null=False,
        blank=False
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users', null=True, blank=False)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
