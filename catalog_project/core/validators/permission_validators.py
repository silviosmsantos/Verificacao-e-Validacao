from django.core.exceptions import ValidationError

def validate_permission_name(value):
    if not value or len(value.strip()) < 3:
        raise ValidationError('O nome da permissão deve ter pelo menos 3 caracteres e não pode ser vazio ou nulo.')
