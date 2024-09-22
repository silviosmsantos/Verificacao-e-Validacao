from django import forms
from core.models.product_models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'status', 'category']

        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'price': 'Preço',
            'image': 'Imagem',
            'status': 'Status',
            'category': 'Categoria',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
