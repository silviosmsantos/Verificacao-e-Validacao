from django.db import models
from core.models.base_model import BaseModel
from core.models.catalog_models import Catalog
from core.validators.message_validator import validate_name, validate_phone

class Message(BaseModel):
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
