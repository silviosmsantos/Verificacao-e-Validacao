import datetime
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.test import TestCase
from core.models.company_models import Company
from core.models.category_models import Category
from core.repositories.product_repository import ProductRepository
from core.validators.product_validators import validate_description, validate_image, validate_name

class ProductRepositoryTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')
        self.category = Category.objects.create(name='Test Category', company=self.company)
        self.repository = ProductRepository()
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 9.99,
            'image': self.create_random_image(),
            'status': 'active',
            'category': self.category
        }
        self.product = self.repository.create_product(self.product_data)

    def create_random_image(self):
        current_date = datetime.datetime.now()
        file_name = f"foto_{current_date.day}_{current_date.month}_{current_date.year}_{current_date.microsecond}.jpg"
        image = Image.new('RGB', (100, 100), color='blue')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        return ContentFile(image_io.read(), file_name)

    def test_create_product(self):
        image_name = self.product.image.name.split('/')[-1]
        self.assertIsNotNone(self.product.id)
        self.assertEqual(self.product.name, self.product_data['name'])
        self.assertTrue(image_name.startswith('foto_'))

    def test_get_product(self):
        fetched_product = self.repository.get_product(self.product.id)
        self.assertEqual(fetched_product.id, self.product.id)
        self.assertEqual(fetched_product.name, self.product.name)

    def test_update_product(self):
        updated_data = {'name': 'Updated Product'}
        updated_product = self.repository.update_product(self.product.id, updated_data)
        self.assertEqual(updated_product.name, updated_data['name'])

    def test_delete_product(self):
        self.repository.delete_product(self.product.id)
        deleted_product = self.repository.get_product(self.product.id)
        self.assertIsNone(deleted_product)

    def test_list_products(self):
        products = self.repository.list_products()
        self.assertIn(self.product, products)

    def test_validate_name(self):
        try:
            validate_name('Valid Product Name')
        except ValidationError:
            self.fail('validate_name() raised ValidationError unexpectedly!')

    def test_validate_name_too_short(self):
        with self.assertRaises(ValidationError):
            validate_name('No')

    def test_validate_description(self):
        try:
            validate_description('Valid description with enough length.')
        except ValidationError:
            self.fail('validate_description() raised ValidationError unexpectedly!')

    def test_validate_description_empty(self):
        with self.assertRaises(ValidationError):
            validate_description('')

    def test_validate_description_too_short(self):
        with self.assertRaises(ValidationError):
            validate_description('Short')

    def test_validate_image(self):
        try:
            validate_image(self.create_random_image())
        except ValidationError:
            self.fail('validate_image() raised ValidationError unexpectedly!')

    def test_validate_image_none(self):
        with self.assertRaises(ValidationError):
            validate_image(None)
