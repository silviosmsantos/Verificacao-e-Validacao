from core.models.message_models import Message
from django.core.exceptions import ObjectDoesNotExist

class MessageRepository:
    @staticmethod
    def create_message(data):
        return Message.objects.create(**data)

    @staticmethod
    def get_message_by_id(message_id):
        try:
            return Message.objects.get(id=message_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update_message(message_id, data):
        try:
            message = Message.objects.get(id=message_id)
            for attr, value in data.items():
                setattr(message, attr, value)
            message.save()
            return message
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_message(message_id):
        try:
            Message.objects.get(id=message_id).delete()
        except ObjectDoesNotExist:
            pass

    @staticmethod
    def list_all_messages():
        return Message.objects.all()
    
    @staticmethod
    def list_messages_by_company(company_id):
        return Message.objects.filter(catalog__company_id=company_id)
