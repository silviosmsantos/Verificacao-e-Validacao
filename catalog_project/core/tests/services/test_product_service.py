import datetime
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models.company_models import Company
from core.models.category_models import Category
from core.services.product_services import ProductService
from core.validators.product_validators import validate_description, validate_image, validate_name

class ProductServiceTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')
        self.category = Category.objects.create(name='Test Category', company=self.company)
        self.service = ProductService()
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 9.99,
            'image': self.create_test_image(),
            'status': 'active',
            'category': self.category
        }
        self.product = self.service.create_product(self.product_data)

    def test_get_product(self):
        fetched_product = self.service.get_product(self.product.id)
        self.assertEqual(fetched_product.id, self.product.id)
        self.assertEqual(fetched_product.name, self.product.name)

    def test_update_product(self):
        updated_data = {'name': 'Updated Product'}
        updated_product = self.service.update_product(self.product.id, updated_data)
        self.assertEqual(updated_product.name, updated_data['name'])

    def test_delete_product(self):
        self.service.delete_product(self.product.id)
        deleted_product = self.service.get_product(self.product.id)
        self.assertIsNone(deleted_product)

    def test_list_products(self):
        products = self.service.list_products()
        self.assertIn(self.product, products)
