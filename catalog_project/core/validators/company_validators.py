from django.core.exceptions import ValidationError

def validate_company_name(value):
    if not value.isalpha():
        raise ValidationError('Company name must contain only alphabetic characters.')
