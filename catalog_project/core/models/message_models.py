from django.db import models
from core.models.base_model import BaseModel
from core.models.catalog_models import Catalog
from core.validators.message_validator import validate_name, validate_phone

class Message(BaseModel):
    """
    Modelo que representa uma mensagem enviada por um usuário.

    Attributes:
        name (str): Nome do remetente da mensagem.
        email (str): E-mail do remetente da mensagem.
        phone (str): Telefone do remetente da mensagem.
        content (str): Conteúdo da mensagem.
        sent_at (datetime): Data e hora em que a mensagem foi enviada.
        catalog (Catalog): Referência ao catálogo associado à mensagem.
    """
    name = models.CharField(max_length=255, null=False, blank=False, validators=[validate_name])
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False, validators=[validate_phone])
    content = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f'{self.name} ({self.email}) - {self.content[:50]}...'
