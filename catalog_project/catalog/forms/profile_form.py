# catalog/forms.py
from django import forms

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=255, label='Name')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Phone')
    status = forms.ChoiceField(choices=[('active', 'Active'), ('inactive', 'Inactive')], label='Status')
