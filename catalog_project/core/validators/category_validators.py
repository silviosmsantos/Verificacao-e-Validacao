from django.core.exceptions import ValidationError

def validate_category_name(value):
    if len(value) < 3:
        raise ValidationError('Category name must be at least 3 characters long.')
