from django.test import TestCase
from core.models.catalog_models import Catalog
from core.models.company_models import Company
from core.models.user_models import User
from core.services.catalog_service import CatalogService

class CatalogServiceTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active')
        self.user = User.objects.create(
            name='Test User',
            email='testuser@example.com',
            phone='1234567890',
            password='password',
            status='active',
            company=self.company
        )
        
        self.catalog_data = {
            'name': 'Test Catalog',
            'status': 'active',
            'company': self.company,
            'user': self.user
        }
        
        self.catalog = CatalogService.create_catalog(self.catalog_data)
        self.assertIsNotNone(self.catalog, "Catalog should be created")
        self.assertEqual(self.catalog.name, 'Test Catalog', "Catalog name should match")

    def test_create_catalog(self):
        catalog_data = {
            'name': 'Another Test Catalog',
            'status': 'inactive',
            'company': self.company,
            'user': self.user
        }
        catalog = CatalogService.create_catalog(catalog_data)
        self.assertIsNotNone(catalog, "Catalog should be created")
        self.assertEqual(catalog.name, 'Another Test Catalog', "Catalog name should match")
        self.assertEqual(catalog.status, 'inactive', "Catalog status should match")
        self.assertEqual(catalog.company, self.company, "Catalog company should match")
        self.assertEqual(catalog.user, self.user, "Catalog user should match")

    def test_update_catalog(self):
        updated_data = {'name': 'Updated Catalog'}
        updated_catalog = CatalogService.update_catalog(self.catalog.id, updated_data)
        
        self.assertEqual(updated_catalog.name, 'Updated Catalog')
        self.assertEqual(updated_catalog.status, 'active')
        self.assertEqual(updated_catalog.company, self.company)
        self.assertEqual(updated_catalog.user, self.user)

    def test_update_catalog_with_invalid_data(self):
        invalid_data = {'name': ''}
        with self.assertRaises(ValueError):
            CatalogService.update_catalog(self.catalog.id, invalid_data)

    def test_delete_catalog(self):
        CatalogService.delete_catalog(self.catalog.id)
        with self.assertRaises(Catalog.DoesNotExist):
            Catalog.objects.get(id=self.catalog.id)
