from django.core.exceptions import ValidationError
import re

def validate_password(value):
    if len(value) < 6:
        raise ValidationError('Password must be at least 6 characters long.')
    if not re.search(r'[A-Za-z]', value) or not re.search(r'[0-9]', value):
        raise ValidationError('Password must contain both letters and numbers.')
