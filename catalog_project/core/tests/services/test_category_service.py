from django.test import TestCase
from core.services.category_service import CategoryService
from core.models.category_models import Category
from core.models.company_models import Company

class CategoryServiceTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active')
        self.category = Category.objects.create(name='Test Category', status='active', company=self.company)

    def test_get_all_categories(self):
        categories = CategoryService.get_all_categories()
        self.assertIn(self.category, categories)

    def test_get_category_by_id(self):
        category = CategoryService.get_category_by_id(self.category.id)
        self.assertEqual(self.category, category)

    def test_create_category(self):
        data = {'name': 'New Category', 'status': 'active', 'company': self.company.id}
        category = CategoryService.create_category(data)
        self.assertEqual(category.name, 'New Category')
        self.assertEqual(category.company, self.company)

    def test_update_category(self):
        data = {'name': 'Updated Category'}
        category = CategoryService.update_category(self.category.id, data)
        self.assertEqual(category.name, 'Updated Category')

    def test_delete_category(self):
        CategoryService.delete_category(self.category.id)
        category = CategoryService.get_category_by_id(self.category.id)
        self.assertIsNone(category)
