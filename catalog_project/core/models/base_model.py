from django.db import models
import uuid
from django.utils import timezone

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        from .user_models import User
        super(BaseModel, self).save(*args, **kwargs)

    modified_by = models.ForeignKey('core.User', on_delete=models.CASCADE, null=True, blank=False, related_name="%(class)s_modified_by")

    class Meta:
        abstract = True
