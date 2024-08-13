from django.core.exceptions import ValidationError
import re

def validate_password(value):
    if len(value) < 8:
        raise ValidationError('A senha deve ter pelo menos 8 caracteres.')
    if not re.search(r'[A-Z]', value):
        raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')
    if not re.search(r'[a-z]', value):
        raise ValidationError('A senha deve conter pelo menos uma letra minúscula.')
    if not re.search(r'[0-9]', value):
        raise ValidationError('A senha deve conter pelo menos um número.')
    if not re.search(r'[@$!%*?&]', value):
        raise ValidationError('A senha deve conter pelo menos um caractere especial: @$!%*?&')
