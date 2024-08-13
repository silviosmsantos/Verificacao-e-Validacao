from django.test import TestCase
from core.models.company_models import Company
from core.models.message_models import Message
from core.models.user_models import User
from core.models.catalog_models import Catalog
from core.services.message_service import MessageService

class MessageServiceTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active')
        self.user = User.objects.create(
            name='Test User',
            email='testuser@example.com',
            phone='1234567890',
            password='password',
            status='active',
            company=None
        )
        self.catalog = Catalog.objects.create(
            name='Test Catalog',
            status='active',
            company=self.company,
            user=self.user
        )
        self.message_data = {
            'content': 'This is a test message',
            'user': self.user,
            'catalog': self.catalog
        }
        self.message = MessageService.create_message(self.message_data)
        self.assertIsNotNone(self.message, "Message should be created")
        self.assertEqual(self.message.content, 'This is a test message', "Message content should match")

    def test_create_message(self):
        message_data = {
            'content': 'Another test message',
            'user': self.user,
            'catalog': self.catalog
        }
        message = MessageService.create_message(message_data)
        self.assertIsNotNone(message, "Message should be created")
        self.assertEqual(message.content, 'Another test message', "Message content should match")

    def test_update_message(self):
        updated_data = {'content': 'Updated message content'}
        updated_message = MessageService.update_message(self.message.id, updated_data)
        self.assertEqual(updated_message.content, 'Updated message content')
        self.assertEqual(updated_message.user, self.user)
        self.assertEqual(updated_message.catalog, self.catalog)

    def test_update_message_with_invalid_data(self):
        invalid_data = {'content': ''}
        with self.assertRaises(ValueError):
            MessageService.update_message(self.message.id, invalid_data)

    def test_delete_message(self):
        MessageService.delete_message(self.message.id)
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(id=self.message.id)
