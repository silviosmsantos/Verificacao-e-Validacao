from ..base_test_case import BaseTestCase
from core.models.message_models import Message
from core.repositories.message_repository import MessageRepository

class MessageRepositoryTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.message_data = self.get_message_data(self.catalog)
        self.message = MessageRepository.create_message(self.message_data)

    def test_create_message(self):
        message_data = self.get_message_data(
            self.catalog,
            name='Another Client',
            email='anotherclient@example.com',
            phone='0987654321',
            content='Another test message'
        )
        message = MessageRepository.create_message(message_data)
        self.assertIsNotNone(message)
        self.assertEqual(message.name, 'Another Client')
        self.assertEqual(message.email, 'anotherclient@example.com')
        self.assertEqual(message.phone, '0987654321')
        self.assertEqual(message.content, 'Another test message')

    def test_get_message_by_id(self):
        message = MessageRepository.get_message_by_id(self.message.id)
        self.assertEqual(message.id, self.message.id)
        self.assertEqual(message.content, 'This is a test message')

    def test_update_message(self):
        updated_data = {'content': 'Updated content'}
        updated_message = MessageRepository.update_message(self.message.id, updated_data)
        self.assertEqual(updated_message.content, 'Updated content')

    def test_delete_message(self):
        MessageRepository.delete_message(self.message.id)
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(id=self.message.id)
