from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password123',
            name='Test User',
            phone='1234567890',
            status='active'
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
        self.assertEqual(response.status_code, 302)  # Espera um redirecionamento
        self.assertIn('_auth_user_id', self.client.session)  # Verifica se o usuário está autenticado

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)  # Verifica se o usuário não está autenticado
