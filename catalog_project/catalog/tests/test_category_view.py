from uuid import uuid4
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from core.models.company_models import Company
from core.models.category_models import Category
from django.utils import timezone
from core.models.user_models import User

class CategoryViewTestCase(TestCase):
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
        self.client.login(email='testuser@example.com', password='securepassword')
        
        self.category = Category.objects.create(
            name='Test Category',
            status='active',
            company=self.company
        )
        self.category_id = self.category.pk

    def test_category_list_view_status_code(self):
        response = self.client.get(reverse('categories_by_company'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

    def test_category_list_view_filter(self):
        response = self.client.get(reverse('categories_by_company'), {'name': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

        response = self.client.get(reverse('categories_by_company'), {'name': 'Invalid'})
        self.assertNotContains(response, 'Test Category')

    def test_category_delete_view_get(self):
        delete_url = reverse('category_delete', args=[self.category.pk])
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
