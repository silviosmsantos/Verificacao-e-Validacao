from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models.company_models import Company
from core.models.catalog_models import Catalog
from core.models.category_models import Category
from core.models.message_models import Message

class HomeViewTestCase(TestCase):
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

        self.client.login(username='testuser@example.com', password='password123')

        self.catalog = Catalog.objects.create(
            name='Test Catalog',
            status='active',
            company=self.company,
            user=self.user
        )
        self.category = Category.objects.create(
            name='Test Category',
            status='active',
            company=self.company
        )
        self.message = Message.objects.create(
            name='Test Name',
            email='test@example.com',
            phone='1234567890',
            content='This is a test message.',
            catalog=self.catalog
        )

        self.home_url = reverse('home')

    def test_home_page_status_code(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_context_data(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['user'], self.user.name)
        self.assertEqual(response.context['catalog_count'], 1)
        self.assertEqual(response.context['category_count'], 1)
        self.assertEqual(response.context['message_count'], 1)
