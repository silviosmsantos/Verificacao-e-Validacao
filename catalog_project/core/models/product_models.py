import os
from django.db import models
from catalog_project.settings import BASE_DIR
from core.validators.product_validators import validate_name, validate_description, validate_image
from .base_model import BaseModel
from core.models.category_models import Category
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location=os.path.join(BASE_DIR, 'media'))

class Product(BaseModel):
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(
        max_length=150, 
        null=False, 
        blank=False,
        validators=[validate_name]
    )
    
    description = models.CharField(
        max_length=300,
        blank=True,
        validators=[validate_description]
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False
    )
    
    image = models.ImageField(
        upload_to='images/',
        storage=fs,
        validators=[validate_image],
        blank=False 
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
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
