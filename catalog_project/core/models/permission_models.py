from django.db import models
from .base_model import BaseModel
from .company_models import Company
from .user_models import User
from core.validators.category_validators import validate_category_name

class Permission(BaseModel):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[validate_category_name]
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permission_users')


    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self):
        return self.name
