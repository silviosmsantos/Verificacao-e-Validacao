from django.core.exceptions import ValidationError

def validate_category_name(value):
    if value is None or value.strip() == '':
        raise ValidationError('O nome da categoria não pode ser nulo ou vazio.')
    if len(value) < 3:
        raise ValidationError('O nome da categoria deve ter pelo menos 3 caracteres.')
