from django.test import TestCase
from core.repositories.category_repository import CategoryRepository
from core.models.category_models import Category
from core.models.company_models import Company

class CategoryRepositoryTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active', email="test@example.com")
        self.category = Category.objects.create(name='Test Category', status='active', company=self.company)

    def test_get_all_categories(self):
        categories = CategoryRepository.get_all_categories()
        self.assertIn(self.category, categories)

    def test_get_category_by_id(self):
        category = CategoryRepository.get_category_by_id(self.category.id)
        self.assertEqual(self.category, category)

    def test_create_category(self):
        data = {'name': 'New Category', 'status': 'active', 'company': self.company.id}
        category = CategoryRepository.create_category(data)
        self.assertEqual(category.name, 'New Category')
        self.assertEqual(category.company, self.company)

    def test_update_category(self):
        data = {'name': 'Updated Category'}
        category = CategoryRepository.update_category(self.category.id, data)
        self.assertEqual(category.name, 'Updated Category')

    def test_delete_category(self):
        CategoryRepository.delete_category(self.category.id)
        category = CategoryRepository.get_category_by_id(self.category.id)
        self.assertIsNone(category)
