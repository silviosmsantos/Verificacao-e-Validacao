from django.conf import settings
from django.db import models
from .user_models import User
from .permission_models import Permission 

class UserPermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'permission')

    def __str__(self):
        return f"{self.user} - {self.permission}"
