from django import forms
from core.models import User, Company

class RegisterForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        empty_label="Nenhuma empresa"
    )
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'password_confirm', 'status', 'company']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
            'status': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Status'}),
            'company': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Empresa'}),
        }
