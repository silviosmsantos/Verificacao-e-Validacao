from core.models.user_models import User
from core.models.company_models import Company

class UserRepository:
    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def create_user(data):
        if 'company' in data:
            data['company'] = Company.objects.get(id=data['company'])
        return User.objects.create(**data)

    @staticmethod
    def update_user(user_id, data):
        if 'company' in data:
            data['company'] = Company.objects.get(id=data['company'])
        user = UserRepository.get_user_by_id(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            user.save()
            return user
        return None

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if user:
            user.delete()
            return True
        return False
