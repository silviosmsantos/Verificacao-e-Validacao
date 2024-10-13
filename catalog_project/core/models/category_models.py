from django.db import models
from .base_model import BaseModel
from .company_models import Company
from core.validators.category_validators import validate_category_name

class Category(BaseModel):
    """
    Modelo que representa uma categoria.

    Attributes:
        name (str): Nome da categoria. Deve ser único e seguir as regras de validação.
        status (str): Status da categoria (ativo ou inativo).
        company (Company): Referência à empresa associada.
    """
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[validate_category_name]
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='category_users')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
