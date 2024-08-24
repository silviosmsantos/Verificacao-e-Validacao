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
