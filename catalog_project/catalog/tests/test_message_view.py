from uuid import uuid4
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from core.models.catalog_models import Catalog
from core.models.company_models import Company
from core.models.message_models import Message
from django.utils import timezone

class MessageViewTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active')
        self.user = get_user_model().objects.create_user(
            name='Test User',
            phone='1234567890',
            status='active',
            email='testuser@example.com',
            password='securepassword',
            company=self.company,
            profile='manager'
        )
        self.catalog = Catalog.objects.create(
            name='Catalog Test', 
            status='active', 
            company=self.company, 
            user=self.user
        )
        self.client.login(email='testuser@example.com', password='securepassword')
        
        self.message = Message.objects.create(
            name='Test Message', 
            email='message@example.com', 
            phone='0987654321',
            content='This is a test message.',
            catalog=self.catalog,
            sent_at=timezone.now()
        )
        self.message_id = self.message.pk

    def test_messages_list_view_status_code(self):
        response = self.client.get(reverse('messages_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Message')

    def test_messages_list_view_filter(self):
        response = self.client.get(reverse('messages_list'), {'nome': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Message')

        response = self.client.get(reverse('messages_list'), {'nome': 'Invalid'})
        self.assertNotContains(response, 'Test Message')

    def test_message_delete_view_get(self):
        delete_url = reverse('message_delete', args=[self.message.pk])
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

    def test_message_delete_view_post(self):
        delete_url = reverse('message_delete', args=[self.message.pk])
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('messages_list'))
        self.assertFalse(Message.objects.filter(pk=self.message.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Mensagem excluída com sucesso.' for msg in messages))

    def test_message_delete_view_non_existent(self):
        non_existent_id = uuid4()
        delete_url = reverse('message_delete', args=[non_existent_id])
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('messages_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Mensagem não encontrada.' for msg in messages))
