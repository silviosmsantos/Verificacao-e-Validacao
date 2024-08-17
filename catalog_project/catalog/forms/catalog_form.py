from django import forms
from core.models.catalog_models import Catalog

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['name', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
