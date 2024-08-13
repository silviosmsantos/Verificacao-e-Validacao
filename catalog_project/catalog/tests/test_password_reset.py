# catalog/tests/test_password_reset.py
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from core.models import User  # Atualize para usar o modelo de usuário personalizado

class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='securepassword'
        )

    def test_password_reset_request(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset.html')
        response = self.client.post(reverse('password_reset'), {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 302)  

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Redefinição de senha em testserver', email.subject)
        self.assertIn('http://testserver/', email.body)  


