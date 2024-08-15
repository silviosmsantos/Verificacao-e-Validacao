from django.test import TestCase
from django.urls import reverse
from django.core import mail
from core.models import User
from core.models.company_models import Company

class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active')
        self.user = User.objects.create_user(
            name='Test User',
            phone='1234567890',
            status='active',
            email='testuser@example.com',
            password='securepassword',
            company=self.company,
            profile='manager' 
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


