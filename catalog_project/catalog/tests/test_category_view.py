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

