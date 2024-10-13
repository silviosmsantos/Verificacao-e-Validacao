from django.conf import settings
from django.db import models
from core.models.base_model import BaseModel
from core.models.company_models import Company

class Catalog(BaseModel):
    """
    Modelo que representa um catálogo.

    Attributes:
        name (str): Nome do catálogo.
        status (str): Status do catálogo (ativo ou inativo).
        company (Company): Referência à empresa associada.
        user (User): Referência ao usuário que criou o catálogo.
    """
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Catalog"
        verbose_name_plural = "Catalogs"

    def __str__(self):
        return self.name
