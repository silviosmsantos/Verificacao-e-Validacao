from django.db import models
from core.models.base_model import BaseModel
from core.models.company_models import Company
from core.models.user_models import User

class Catalog(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='active',
        max_length=10,
        null=False,
        blank=False
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Catalog"
        verbose_name_plural = "Catalogs"

    def __str__(self):
        return self.name
