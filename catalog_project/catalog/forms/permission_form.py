# catalog/forms/permission_form.py
from django import forms
from core.models.permission_models import Permission

class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['name', 'status']
        labels = {
            'name': 'Nome da Permissão',
            'status': 'Status'
        }
