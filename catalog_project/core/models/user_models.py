from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from .base_model import BaseModel
from .company_models import Company

class User(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True, validators=[EmailValidator("Enter a valid email address.")], blank=False, null=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    password = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value=6, message="Password must be at least 6 characters.")], null=False, blank=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"