from django.test import TestCase
from core.models.company_models import Company
from core.models.user_models import User
from core.models.catalog_models import Catalog
from core.models.category_models import Category
from core.models.product_models import Product
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.company = self.create_company()
        self.user = self.create_user_manager(self.company)
        self.user_manager = self.create_user_admin(self.company)
        self.catalog = self.create_catalog(self.company, self.user)
        self.category = self.create_category()
        self.product_data = self.get_product_data()

    def create_company(self):
        return Company.objects.create(name='Test Company', status='active', email="test@example.com")

    def create_user_manager(self, company):
        return User.objects.create(
            name='Test User',
            email='testuser@example.com',
            phone='1234567890',
            password='password',
            status='active',
            company=company,
            profile='manager'
        )
    
    def create_user_admin(self, company):
        return User.objects.create(
            name='Test User',
            email='testuser123@example.com',
            phone='1234567890',
            password='password',
            status='active',
            company=company,
            profile='admin'
        )

    def create_catalog(self, company, user):
        return Catalog.objects.create(
            name='Test Catalog',
            status='active',
            company=company,
            user=user
        )

    def create_category(self):
        return Category.objects.create(name='Test Category', company=self.company)

    def create_test_image(self):
        image = BytesIO()
        img = Image.new('RGB', (100, 100), color=(73, 109, 137))
        img.save(image, 'PNG')
        image.seek(0)
        return ContentFile(image.read(), 'test_image.png')

    def get_product_data(self):
        return {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 9.99,
            'image': self.create_test_image(),
            'status': 'active',
            'category': self.category,
            'catalog': self.catalog
        }

    def get_message_data(self, catalog=None, name='Client Name', email='client@example.com', phone='1234567890', content='This is a test message'):
        catalog = catalog or self.catalog
        return {
            'name': name,
            'email': email,
            'phone': phone,
            'content': content,
            'catalog': catalog
        }
