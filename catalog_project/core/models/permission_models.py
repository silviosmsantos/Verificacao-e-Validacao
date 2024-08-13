from django.conf import settings
from django.db import models
from .base_model import BaseModel
from .user_models import User
from core.validators.permission_validators import validate_permission_name

class Permission(BaseModel):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[validate_permission_name]
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self):
        return self.name
