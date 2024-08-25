from django import forms
from django.core.exceptions import ValidationError
from core.models.company_models import Company

    
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email']
        labels = {
            'name': 'Nome da Empresa',
            'email': 'E-mail'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }
