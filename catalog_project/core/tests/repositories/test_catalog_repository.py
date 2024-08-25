from django.test import TestCase
from core.repositories.catalog_repository import CatalogRepository
from core.models.catalog_models import Catalog
from core.models.company_models import Company
from core.models.user_models import User

class CatalogRepositoryTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            status="active",
            email="test@example.com"
        )
        self.user = User.objects.create(
            name="Test User",
            email="user@example.com",
            phone="1234567890",
            password="password",
            status="active",
            company=self.company
        )
        self.catalog_data = {
            'name': 'Test Catalog',
            'status': 'active',
            'company': self.company,
            'user': self.user
        }

    def test_create_catalog(self):
        catalog = CatalogRepository.create_catalog(self.catalog_data)
        self.assertIsInstance(catalog, Catalog)
        self.assertEqual(catalog.name, 'Test Catalog')

    def test_get_catalog_by_id(self):
        catalog = CatalogRepository.create_catalog(self.catalog_data)
        fetched_catalog = CatalogRepository.get_catalog_by_id(catalog.id)
        self.assertEqual(catalog, fetched_catalog)

    def test_update_catalog(self):
        catalog = CatalogRepository.create_catalog(self.catalog_data)
        updated_data = {'name': 'Updated Catalog'}
        updated_catalog = CatalogRepository.update_catalog(catalog.id, updated_data)
        self.assertEqual(updated_catalog.name, 'Updated Catalog')

    def test_delete_catalog(self):
        catalog = CatalogRepository.create_catalog(self.catalog_data)
        CatalogRepository.delete_catalog(catalog.id)
        deleted_catalog = CatalogRepository.get_catalog_by_id(catalog.id)
        self.assertIsNone(deleted_catalog)
