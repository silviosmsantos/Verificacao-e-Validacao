from django import forms
from core.models import User, Company

class RegisterForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        empty_label="Nenhuma empresa"  # Opcional
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'status', 'company']
