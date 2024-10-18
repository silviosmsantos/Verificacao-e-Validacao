from django import forms
from core.models.user_models import User

class UserFilterForm(forms.Form):
  
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
    ]

    PROFILE_CHOICES = [
        ('admin', 'Administrador'),
    ]

    name = forms.CharField(label='Nome', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nome do usuário'
    }))
    email = forms.EmailField(label='E-mail', required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'E-mail do usuário'
    }))
    status = forms.ChoiceField(label='Status', choices=STATUS_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    profile = forms.ChoiceField(label='Perfil', choices=PROFILE_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    def filter_users(self, users):
        if self.cleaned_data['name']:
            users = users.filter(name__icontains=self.cleaned_data['name'])

        if self.cleaned_data['email']:
            users = users.filter(email__icontains=self.cleaned_data['email'])

        if self.cleaned_data['status']:
            users = users.filter(status=self.cleaned_data['status'])

        if self.cleaned_data['profile']:
            users = users.filter(profile=self.cleaned_data['profile'])

        return users
