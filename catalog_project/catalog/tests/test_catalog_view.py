from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Company, Catalog

User = get_user_model()

class CatalogViewsTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name='Test Company',
            status='active',
            email='testecompony@gmail.com'
        )
        self.user = get_user_model().objects.create_user(
            name='Test User',
            phone='1234567890',
            status='active',
            email='testuser@example.com',
            password='securepassword',
            company=self.company,
            profile='admin'
        )
        self.catalog = Catalog.objects.create(
            name='Test Catalog', 
            status='active', 
            company=self.company,
            user = self.user
          )
        
        self.client.login(email='testuser@example.com', password='securepassword')

    

