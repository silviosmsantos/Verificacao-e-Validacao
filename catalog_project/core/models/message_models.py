from django.db import models
from django.conf import settings
from core.models.base_model import BaseModel
from core.models.catalog_models import Catalog

class Message(BaseModel):
    content = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f'{self.content[:50]}... by {self.user.name} at {self.sent_at}'
