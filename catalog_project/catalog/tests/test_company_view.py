from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from core.models import Company

class CompanyRegisterViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('company_register')

    def test_company_register_success(self):
        response = self.client.post(self.url, {
            'name': 'Test Company',
            'email': 'testcompany@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(Company.objects.filter(email='testcompany@example.com').exists())

    def test_company_register_duplicate_email(self):
        Company.objects.create(name='Existing Company', email='duplicate@example.com', status='active')

        response = self.client.post(self.url, {
            'name': 'New Company',
            'email': 'duplicate@example.com',
        })

        # Verifique se o status da resposta é 200, indicando que o formulário foi renderizado novamente
        self.assertEqual(response.status_code, 200)
        
        # Verifique se o formulário não é válido
        form = response.context['form']
        self.assertFalse(form.is_valid())

        