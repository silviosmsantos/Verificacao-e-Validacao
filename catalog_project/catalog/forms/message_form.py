from django import forms

class MessageFilterForm(forms.Form):
    nome = forms.CharField(required=False, label='Nome')
    email = forms.EmailField(required=False, label='Email')
    phone = forms.CharField(required=False, label='Telefone')
    sent_at = forms.DateField(required=False, label='Data de Envio', widget=forms.DateInput(attrs={'type': 'date'}))
