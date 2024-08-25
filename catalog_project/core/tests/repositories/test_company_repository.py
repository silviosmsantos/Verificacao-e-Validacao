from django.test import TestCase
from core.models.company_models import Company
from core.repositories.company_repository import CompanyRepository

class CompanyRepositoryTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active',email="test@example.com")

    def test_get_all_companies(self):
        companies = CompanyRepository.get_all_companies()
        self.assertIn(self.company, companies)

    def test_get_company_by_id(self):
        company = CompanyRepository.get_company_by_id(self.company.id)
        self.assertEqual(self.company, company)

    def test_create_company(self):
        data = {'name': 'New Company', 'status': 'active', 'email': 'test2@example.com'}
        company = CompanyRepository.create_company(data)
        self.assertEqual(company.name, 'New Company')

    def test_update_company(self):
        data = {'name': 'Updated Company'}
        company = CompanyRepository.update_company(self.company.id, data)
        self.assertEqual(company.name, 'Updated Company')

    def test_delete_company(self):
        CompanyRepository.delete_company(self.company.id)
        company = CompanyRepository.get_company_by_id(self.company.id)
        self.assertIsNone(company)
