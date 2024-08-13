from audioop import reverse
from unittest import TestCase
from django.contrib.auth import get_user_model


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password123',
            name='Test User',
            phone='1234567890',
            status='active'
        )
        self.profile_url = reverse('profile')
        self.client.login(email='testuser@example.com', password='password123')

    def test_profile_page_status_code(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_profile_form_initial_data(self):
        response = self.client.get(self.profile_url)
        self.assertContains(response, 'Test User')
        self.assertContains(response, 'testuser@example.com')
        self.assertContains(response, '1234567890')

    def test_update_profile_with_valid_data(self):
        updated_data = {
            'name': 'Updated Name',
            'email': 'updated@example.com',
            'phone': '0987654321',
            'status': 'active',  # Mesmo que o campo seja desativado no formulário, ele ainda faz parte dos dados.
            'company': '',  # Use uma string vazia em vez de None
        }
        response = self.client.post(self.profile_url, updated_data)
        self.assertEqual(response.status_code, 302)  # Espera um redirecionamento após a atualização

        # Verifica se os dados foram atualizados
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated Name')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.phone, '0987654321')

    def test_update_profile_with_invalid_data(self):
        invalid_data = {
            'name': '',  # Nome vazio, que deve ser inválido
            'email': 'invalid-email',  # Email inválido
            'phone': 'invalid-phone',  # Telefone inválido
            'status': 'active',
            'company': '',  # Use uma string vazia em vez de None
        }
        response = self.client.post(self.profile_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Espera-se que a página seja recarregada sem redirecionamento

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.name, '')
        self.assertNotEqual(self.user.email, 'invalid-email')
        self.assertNotEqual(self.user.phone, 'invalid-phone')

    def test_profile_page_requires_login(self):
        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302) 
