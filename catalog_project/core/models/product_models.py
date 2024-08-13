from django.db import models
from .base_model import BaseModel 
from ..validators.product_validator import validate_product_name
from core.models.category_models import Category  # Certifique-se de que Category está importado

class Product(BaseModel):
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(
        max_length=150, 
        null=False, 
        blank=False,
        validators=[validate_product_name]
    )
    
    description = models.CharField(
        max_length=300,
        blank=True,
        null=True,
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False
    )
    
    image = models.CharField(
        null=True,
        blank=True,
        max_length=400
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=False,
        blank=False
    )
    
    class Meta:
        verbose_name ='Product'
        verbose_name_plural = 'Products'
