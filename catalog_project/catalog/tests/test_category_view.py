from uuid import uuid4
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from core.models.company_models import Company
from core.models.category_models import Category
from django.utils import timezone
from core.models.user_models import User

class CategoryViewTestCase(TestCase):
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
        self.client.login(email='testuser@example.com', password='securepassword')
        
        self.category = Category.objects.create(
            name='Test Category',
            status='active',
            company=self.company
        )
        self.category_id = self.category.pk

    def test_category_list_view_status_code(self):
        response = self.client.get(reverse('categories_by_company'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

    def test_category_list_view_filter(self):
        response = self.client.get(reverse('categories_by_company'), {'name': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

        response = self.client.get(reverse('categories_by_company'), {'name': 'Invalid'})
        self.assertNotContains(response, 'Test Category')

    def test_category_delete_view_get(self):
        delete_url = reverse('category_delete', args=[self.category.pk])
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

    def test_category_delete_view_post(self):
        delete_url = reverse('category_delete', args=[self.category.pk])
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('categories_by_company'))
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'category excluída com sucesso.' for msg in messages))

    def test_category_delete_view_non_existent(self):
        non_existent_id = uuid4()
        delete_url = reverse('category_delete', args=[non_existent_id])
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('categories_by_company'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Category não encontrada.' for msg in messages))

    def test_category_create_view(self):
        create_url = reverse('category_create')
        response = self.client.post(create_url, {
            'name': 'New Category',
            'status': 'active',
            'company': self.company.pk 
        })
        self.assertRedirects(response, reverse('categories_by_company'))
        self.assertTrue(Category.objects.filter(name='New Category').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Categoria criada com sucesso.' for msg in messages))

    def test_category_edit_view_get(self):
        edit_url = reverse('category_edit', args=[self.category.pk])
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_category_edit_view_post(self):
        edit_url = reverse('category_edit', args=[self.category.pk])
        response = self.client.post(edit_url, {
            'name': 'Updated Category',
            'status': 'inactive',
            'company': self.company.pk 
        })
        self.assertRedirects(response, reverse('categories_by_company'))
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')
        self.assertEqual(self.category.status, 'inactive')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Categoria atualizada com sucesso.' for msg in messages))
