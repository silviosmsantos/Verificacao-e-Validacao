from django.test import TestCase
from core.services.company_service import CompanyService
from core.models.company_models import Company

class CompanyServiceTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active')

    def test_get_all_companies(self):
        companies = CompanyService.get_all_companies()
        self.assertIn(self.company, companies)

    def test_get_company_by_id(self):
        company = CompanyService.get_company_by_id(self.company.id)
        self.assertEqual(self.company, company)

    def test_create_company(self):
        data = {'name': 'New Company', 'status': 'active'}
        company = CompanyService.create_company(data)
        self.assertEqual(company.name, 'New Company')

    def test_update_company(self):
        data = {'name': 'Updated Company'}
        company = CompanyService.update_company(self.company.id, data)
        self.assertEqual(company.name, 'Updated Company')

    def test_delete_company(self):
        CompanyService.delete_company(self.company.id)
        company = CompanyService.get_company_by_id(self.company.id)
        self.assertIsNone(company)
