from django import forms
from core.models.user_models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'status', 'company', 'profile']
        
        labels = {
            'email': 'E-mail',
            'name': 'Nome',
            'phone': 'Telefone',
            'status': 'Status',
            'company': 'Empresa',
            'profile': 'Perfil',
        }

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'profile': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['company'].initial = user.company
