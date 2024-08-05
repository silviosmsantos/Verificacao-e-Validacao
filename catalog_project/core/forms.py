from django import forms
from core.models.category_models import Category
from core.models.company_models import Company
from core.models.user_models import User
from core.validators.category_validators import validate_category_name
from core.validators.company_validators import validate_company_name
from core.validators.user_validators import validate_password

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'status', 'company']
        widgets = {
            'status': forms.Select(choices=Category.STATUS_CHOICES),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'status']
        widgets = {
            'status': forms.Select(choices=Company.STATUS_CHOICES),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'status', 'company']
        widgets = {
            'status': forms.Select(choices=User.STATUS_CHOICES),
        }
