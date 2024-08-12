from core.models.message_models import Message

class MessageRepository:
    @staticmethod
    def create_message(data):
        return Message.objects.create(**data)

    @staticmethod
    def get_message_by_id(message_id):
        return Message.objects.get(id=message_id)

    @staticmethod
    def update_message(message_id, data):
        message = Message.objects.get(id=message_id)
        for attr, value in data.items():
            setattr(message, attr, value)
        message.save()
        return message

    @staticmethod
    def delete_message(message_id):
        Message.objects.get(id=message_id).delete()
