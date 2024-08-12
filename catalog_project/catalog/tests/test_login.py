# catalog/tests/test_login.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.email = 'testuser@example.com'
        self.password = 'securepassword'
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            username=self.email
        )

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': self.email,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('home'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Bem-vindo(a), {self.user.email}')

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'wronguser@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Email ou senha inválidos')

