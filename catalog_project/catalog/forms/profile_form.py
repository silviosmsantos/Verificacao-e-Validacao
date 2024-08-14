from django import forms
from core.models.company_models import Company

class ProfileForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
        label="Nome"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        label="E-mail",
        required=False  # Define como não obrigatório para evitar mensagens de erro
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
        label="Telefone"
    )
    status = forms.ChoiceField(
        choices=[('active', 'Ativo'), ('inactive', 'Inativo')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        label="Empresa",
        required=False  # Define como não obrigatório para evitar mensagens de erro
    )

    def clean_email(self):
        # Retorna o valor inicial do email se o campo estiver desativado
        return self.initial.get('email', '')

    def clean_company(self):
        # Retorna o valor inicial da empresa se o campo estiver desativado
        return self.initial.get('company', '')
