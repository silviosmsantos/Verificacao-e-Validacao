from django.core.exceptions import ValidationError
import re

def validate_name(value):
    if value is None or len(value) < 3:
        raise ValidationError('O nome deve ter pelo menos 3 caracteres.')

def validate_phone(value):
    if value is not None and not re.match(r'^\+?1?\d{9,15}$', value):
        raise ValidationError('O telefone deve conter apenas números e pode incluir um código de país.')

def validate_message_data(data, is_update=False):
    if not is_update:
        validate_name(data.get('name'))
    if 'phone' in data:
        validate_phone(data.get('phone'))
