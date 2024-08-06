# core/services/message_service.py
from core.repositories.message_repository import MessageRepository
from core.validators.message_validator import validate_message_data

class MessageService:
    @staticmethod
    def create_message(data):
        validate_message_data(data)
        return MessageRepository.create_message(data)

    @staticmethod
    def get_message(message_id):
        return MessageRepository.get_message_by_id(message_id)

    @staticmethod
    def update_message(message_id, data):
        validate_message_data(data, is_update=True)
        return MessageRepository.update_message(message_id, data)

    @staticmethod
    def delete_message(message_id):
        return MessageRepository.delete_message(message_id)
