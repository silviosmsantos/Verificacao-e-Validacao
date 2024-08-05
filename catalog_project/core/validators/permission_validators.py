from django.core.exceptions import ValidationError

def validate_permission_name(value):
    if not value or len(value.strip()) < 3:
        raise ValidationError('Permission name must be at least 3 characters long and cannot be empty or null.')
