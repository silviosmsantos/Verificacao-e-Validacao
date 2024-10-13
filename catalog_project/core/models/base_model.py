from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone

class BaseModel(models.Model):
    """
    Modelo base que fornece campos comuns para outros modelos.

    Attributes:
        id (UUID): Identificador único do modelo.
        created_at (datetime): Data e hora de criação do registro.
        updated_at (datetime): Data e hora da última atualização do registro.
        modified_by (User): Referência ao usuário que modificou o registro.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_modified_by"
    )

    class Meta:
        abstract = True
