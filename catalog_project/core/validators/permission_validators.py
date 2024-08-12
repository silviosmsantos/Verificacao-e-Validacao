from django.core.exceptions import ValidationError

def validate_permission_name(value):
    if not value or len(value.strip()) < 3:
        raise ValidationError('Permission name must be at least 3 characters long and cannot be empty or null.')

def validate_category_permission(user):
    if not user.has_perm('your_app_name.manage_category'):
        raise ValidationError("You do not have permission to manage categories.")

def validate_company_permission(user):
    if not user.has_perm('your_app_name.manage_company'):
        raise ValidationError("You do not have permission to manage companies.")

 