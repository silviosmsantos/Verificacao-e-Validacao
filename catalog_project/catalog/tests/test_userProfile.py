from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from core.models.company_models import Company

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password123',
            name='Test User',
            phone='1234567890',
            status='active',
            company=self.company,
            profile='manage'
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
        self.assertContains(response, 'manage')

    def test_update_profile_with_invalid_data(self):
        invalid_data = {
            'name': '', 
            'phone': 'invalid-phone',  
            'status': 'active',
            'profile': 'user'
        }
        response = self.client.post(self.profile_url, invalid_data)
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.name, '')
        self.assertNotEqual(self.user.phone, 'invalid-phone')
