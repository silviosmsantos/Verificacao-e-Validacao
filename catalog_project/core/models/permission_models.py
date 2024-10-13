from django.db import models
from .base_model import BaseModel
from core.validators.permission_validators import validate_permission_name

class Permission(BaseModel):
    """
    Modelo que representa uma permissão no sistema.

    Attributes:
        name (str): Nome da permissão.
        status (str): Status da permissão (ativo ou inativo).
    """
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[validate_permission_name]
    )
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )
    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self):
        return self.name
