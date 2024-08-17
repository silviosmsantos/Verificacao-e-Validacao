from django.test import TestCase
from core.models.company_models import Company
from core.models.user_models import User
from core.models.catalog_models import Catalog

class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.company = self.create_company()
        self.user = self.create_user(self.company)
        self.catalog = self.create_catalog(self.company, self.user)

    def create_company(self):
        return Company.objects.create(name='Test Company', status='active')

    def create_user(self, company):
        return User.objects.create(
            name='Test User',
            email='testuser@example.com',
            phone='1234567890',
            password='password',
            status='active',
            company=company,
            profile='manager'
        )

    def create_catalog(self, company, user):
        return Catalog.objects.create(
            name='Test Catalog',
            status='active',
            company=company,
            user=user
        )

    def get_message_data(self, catalog=None, name='Client Name', email='client@example.com', phone='1234567890', content='This is a test message'):
        catalog = catalog or self.catalog
        return {
            'name': name,
            'email': email,
            'phone': phone,
            'content': content,
            'catalog': catalog
        }
