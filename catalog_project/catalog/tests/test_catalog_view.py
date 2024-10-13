import json
import uuid
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Company, Catalog
from core.models.category_models import Category
from core.models.product_models import Product

class CatalogViewsTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name='Test Company',
            status='active',
            email='testecompony@gmail.com'
        )
        self.user = get_user_model().objects.create_user(
            name='Test User',
            phone='1234567890',
            status='active',
            email='testuser@example.com',
            password='securepassword',
            company=self.company,
            profile='admin'
        )
        self.catalog = Catalog.objects.create(
            name='Test Catalog', 
            status='active', 
            company=self.company,
            user=self.user
        )
        self.category = Category.objects.create(name='Test Category', status='active', company=self.company)

        self.client.login(email='testuser@example.com', password='securepassword')

    def test_catalog_company_visualize_product(self):
        response = self.client.get(reverse('catalog_company_visualize_product'), {'company_id': self.company.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog_company_visualize_product.html')
        self.assertIn('companies', response.context)
        self.assertIn('catalogs', response.context)
        self.assertEqual(response.context['selected_company'], self.company)

    def test_catalog_list_view(self):
        response = self.client.get(reverse('catalog_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog_list.html')

        self.assertIn('catalogs', response.context)
        
        catalogs = response.context['catalogs']
        self.assertEqual(catalogs.count(), 1)
        self.assertEqual(catalogs.first(), self.catalog)

    def test_catalog_detail_view_without_catalog_id(self):
        response = self.client.get(reverse('catalog_detail'))
        self.assertEqual(response.status_code, 302)

    def test_catalog_detail_view_with_valid_catalog_id(self):
        response = self.client.get(reverse('catalog_detail'), {'catalog_id': self.catalog.id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog_detail.html')

        self.assertIn('catalog', response.context)
        self.assertIn('products', response.context)

        catalog = response.context['catalog']
        self.assertEqual(catalog, self.catalog)

    def test_catalog_detail_view_with_invalid_catalog_id(self):
        invalid_uuid = uuid.uuid4()
        response = self.client.get(reverse('catalog_detail'), {'catalog_id': invalid_uuid})
        self.assertEqual(response.status_code, 302)

    def test_get_products_by_catalog_view(self):
        _ = Product.objects.create(
            name='Product 1',
            price=100.0,
            catalog=self.catalog,
            status='active',
            description='A product description',
            category=self.category
        )

        response = self.client.get(reverse('get_products_by_catalog', kwargs={'catalog_id': self.catalog.id}))

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('products', response_data)
        self.assertEqual(len(response_data['products']), 1)
        self.assertEqual(response_data['products'][0]['name'], 'Product 1')

    def test_catalog_create_view_create_new_catalog(self):
        response = self.client.post(reverse('catalog_create'), {
            'name': 'New Catalog',
            'status': 'active'
        })
        self.assertEqual(response.status_code, 200)
        new_catalog = Catalog.objects.get(name='New Catalog')
        self.assertIsNotNone(new_catalog)
        self.assertEqual(new_catalog.status, 'active')
        self.assertEqual(new_catalog.company, self.company)
        self.assertEqual(new_catalog.user, self.user)

    def test_catalog_create_view_edit_existing_catalog(self):
        response = self.client.post(reverse('catalog_edit', kwargs={'catalog_id': self.catalog.id}), {
            'name': 'Updated Catalog',
            'status': 'inactive'
        })
        self.assertEqual(response.status_code, 200)
        updated_catalog = Catalog.objects.get(id=self.catalog.id)
        self.assertEqual(updated_catalog.name, 'Updated Catalog')
        self.assertEqual(updated_catalog.status, 'inactive')
        self.assertEqual(updated_catalog.company, self.company)
        self.assertEqual(updated_catalog.user, self.user)

    def test_add_products_view_get_request(self):
        response = self.client.get(reverse('add_products', kwargs={'catalog_id': self.catalog.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_products.html')

        self.assertIn('catalog', response.context)
        self.assertIn('formset', response.context)
        self.assertIn('categories', response.context)

    def test_save_products_view_valid_data(self):
        product_data = [
            {
                'name': 'Product 1',
                'price': 100.0,
                'description': 'Description for product 1',
                'category': str(self.category.id),  
                'status': 'active',
                'image': None  
            },
            {
                'name': 'Product 2',
                'price': 150.0,
                'description': 'Description for product 2',
                'category': str(self.category.id), 
                'status': 'active',
                'image': None 
            }
        ]

        response = self.client.post(
            reverse('save_products', kwargs={'catalog_id': self.catalog.id}),
            json.dumps({'product_data': product_data}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

        products = Product.objects.filter(catalog=self.catalog)
        self.assertEqual(products.count(), 2)
        self.assertEqual(products[0].name, 'Product 1')
        self.assertEqual(products[1].name, 'Product 2')

    def test_save_products_view_invalid_category(self):
        invalid_uuid = uuid.uuid4()
        product_data = [
            {
                'name': 'Product 1',
                'price': 100.0,
                'description': 'Description for product 1',
                'category': str(invalid_uuid),
                'status': 'active',
                'image': None  
            }
        ]

        response = self.client.post(
            reverse('save_products', kwargs={'catalog_id': self.catalog.id}),
            json.dumps({'product_data': product_data}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500) 
