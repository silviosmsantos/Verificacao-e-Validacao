from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models.company_models import Company
from core.models.user_models import User
import uuid

class UserViewsTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active')
        
        self.manager_user = get_user_model().objects.create_user(
            name='Manager User',
            phone='1234567890',
            status='active',
            email='manager@example.com',
            password='securepassword',
            company=self.company,
            profile='manager'
        )
        
        self.normal_user = get_user_model().objects.create_user(
            name='Normal User',
            phone='0987654321',
            status='active',
            email='user@example.com',
            password='securepassword',
            company=self.company,
            profile='user'
        )
        
        self.client.login(email='manager@example.com', password='securepassword')

    def test_user_list_view(self):
        response = self.client.get(reverse('user_list_company'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list_company.html')
        self.assertContains(response, 'Usuários da Empresa Test Company')

    def test_user_delete_view(self):
        response = self.client.post(reverse('user_delete', kwargs={'pk': self.normal_user.id}))
        self.assertRedirects(response, reverse('user_list_company'))
        self.assertFalse(User.objects.filter(id=self.normal_user.id).exists())
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Usuário excluído com sucesso.')

    def test_user_delete_view_user_not_found(self):
        invalid_uuid = uuid.uuid4()
        response = self.client.post(reverse('user_delete', kwargs={'pk': invalid_uuid}))
        self.assertRedirects(response, reverse('user_list_company'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Usuário não encontrado.')
