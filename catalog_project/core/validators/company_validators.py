from django.core.exceptions import ValidationError

def validate_company_name(value):
    if not value:
        raise ValidationError('O nome da empresa não pode ser nulo ou vazio.')
    if not value.isalpha():
        raise ValidationError('O nome da empresa deve conter apenas caracteres alfabéticos.')
