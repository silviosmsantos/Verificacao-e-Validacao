from django import forms
from core.models.catalog_models import Catalog

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['name', 'status']

        labels = {
            'name': 'Nome',
            'status': 'Status',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
