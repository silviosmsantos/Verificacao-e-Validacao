import os
from django.db import models
from django.core.files.storage import default_storage
from catalog_project.settings import BASE_DIR
from core.models.catalog_models import Catalog
from core.validators.product_validators import validate_name, validate_description, validate_image
from .base_model import BaseModel
from core.models.category_models import Category
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location=os.path.join(BASE_DIR, 'media/images'))

class Product(BaseModel):
    """
    Modelo que representa um produto no sistema.

    Attributes:
        name (str): Nome do produto.
        description (str): Descrição do produto.
        price (Decimal): Preço do produto.
        image (ImageField): Imagem do produto.
        status (str): Status do produto (ativo ou inativo).
        category (Category): Categoria associada ao produto.
        catalog (Catalog): Catálogo associado ao produto.
    """
    
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
        related_name='products_category',
        null=False,
        blank=False
    )

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        related_name='products_catalog',
        null=False,
        blank=False
    )
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            file_path = fs.save(self.image.name, self.image)
            print(f'File saved at: {file_path}')