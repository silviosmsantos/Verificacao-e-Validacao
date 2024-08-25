from django import forms
from core.models import Message

class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Seu Nome',
            'email': 'Seu Email',
            'phone': 'Seu Telefone',
            'content': 'Sua Mensagem',
        }
