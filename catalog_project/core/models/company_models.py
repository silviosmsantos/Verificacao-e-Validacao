from django.db import models
from .base_model import BaseModel
from core.validators.company_validators import validate_company_name

class Company(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(
        max_length=255,
        validators=[validate_company_name]
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
