# core/models/catalog_models.py
from django import forms
from core.models.category_models import Category  # Ajuste o import conforme sua estrutura

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
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
