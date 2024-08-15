from django.test import TestCase
from core.models.company_models import Company
from core.models.message_models import Message
from core.models.user_models import User
from core.models.catalog_models import Catalog
from core.repositories.message_repository import MessageRepository

class MessageRepositoryTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active')
        self.user = User.objects.create(
            name='Test User',
            email='testuser@example.com',
            phone='1234567890',
            password='password',
            status='active',
            company=self.company,
            profile='manager' 
        )
        self.catalog = Catalog.objects.create(
            name='Test Catalog',
            status='active',
            company=self.company,
            user=self.user
        )
        self.message_data = {
            'content': 'Test message content',
            'user': self.user,
            'catalog': self.catalog
        }
        self.message = MessageRepository.create_message(self.message_data)

    def test_create_message(self):
        message_data = {
            'content': 'Another test message',
            'user': self.user,
            'catalog': self.catalog
        }
        message = MessageRepository.create_message(message_data)
        self.assertIsNotNone(message, "Message should be created")
        self.assertEqual(message.content, 'Another test message', "Message content should match")

    def test_get_message_by_id(self):
        message = MessageRepository.get_message_by_id(self.message.id)
        self.assertEqual(message.id, self.message.id, "Retrieved message ID should match")
        self.assertEqual(message.content, 'Test message content', "Retrieved message content should match")

    def test_update_message(self):
        updated_data = {'content': 'Updated content'}
        updated_message = MessageRepository.update_message(self.message.id, updated_data)
        self.assertEqual(updated_message.content, 'Updated content', "Updated message content should match")

    def test_update_message_with_invalid_id(self):
        invalid_id = 999999
        updated_data = {'content': 'Updated content'}
        with self.assertRaises(Message.DoesNotExist):
            MessageRepository.update_message(invalid_id, updated_data)

    def test_delete_message(self):
        MessageRepository.delete_message(self.message.id)
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(id=self.message.id)

    def test_delete_message_with_invalid_id(self):
        invalid_id = 999999
        with self.assertRaises(Message.DoesNotExist):
            MessageRepository.delete_message(invalid_id)
