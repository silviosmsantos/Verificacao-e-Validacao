from django.db import models
import uuid
from django.utils import timezone

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    modified_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_modified_by")

    class Meta:
        abstract = True
