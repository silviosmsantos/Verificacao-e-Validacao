from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models.company_models import Company 

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')
        
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password123',
            name='Test User',
            phone='1234567890',
            status='active',
            company=self.company,
            profile='manager' 
        )
        self.login_url = reverse('login')

    def test_login_page_status_code(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
