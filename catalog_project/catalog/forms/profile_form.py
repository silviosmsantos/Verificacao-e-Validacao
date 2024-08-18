from django import forms
from core.models.user_models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'status', 'company', 'profile']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'company': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'profile': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['status'].disabled = True
        self.fields['company'].disabled = True
        self.fields['profile'].disabled = True
