import re
from django import forms
from core.models import User, Company

class RegisterForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'}),
        label="Confirmar Senha",
        required=True
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Empresa"
    )
    profile = forms.ChoiceField(
        choices=User.PROFILE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Perfil"
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'password_confirm', 'status', 'company', 'profile']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Nome *',
            'email': 'E-mail *',
            'phone': 'Telefone *',
            'password': 'Senha *',
            'status': 'Status *',
            'company': 'Empresa *',
            'profile': 'Perfil *',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\d+$', phone):
            self.add_error('phone', "O telefone deve conter apenas números.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            forms.EmailField().clean(email)
        except forms.ValidationError:
            self.add_error('email', "O e-mail fornecido não é válido.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 6:
                self.add_error('password', "A senha deve ter pelo menos 6 caracteres.")
            if re.search(r'[^\w\s]', password):
                self.add_error('password', "A senha não deve conter caracteres especiais.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem.")

        return cleaned_data
