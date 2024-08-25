from django import forms
from django.forms import inlineformset_factory
from core.models.catalog_models import Catalog
from core.models.product_models import Product

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

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', [])
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = categories

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'status', 'category']
        labels = {
            'name': 'Nome do Produto',
            'description': 'Descrição',
            'price': 'Preço',
            'image': 'Imagem',
            'status': 'Status',
            'category': 'Categoria',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

ProductFormSet = inlineformset_factory(Catalog, Product, form=ProductForm, extra=1, can_delete=True)
