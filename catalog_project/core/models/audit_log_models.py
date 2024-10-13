from django.db import models
from .base_model import BaseModel
from .user_models import User

class AuditLog(BaseModel):
    """
    Modelo que representa um log de auditoria.

    Attributes:
        action (str): Ação realizada (criação, atualização ou exclusão).
        timestamp (datetime): Data e hora em que a ação foi realizada.
        user (User): Referência ao usuário que realizou a ação.
    """
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "AuditLog"
        verbose_name_plural = "AuditLogs"

    def __str__(self):
        return f'{self.action} by {self.user.name} at {self.timestamp}'
