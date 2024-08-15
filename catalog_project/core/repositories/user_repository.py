from core.models.company_models import Company
from core.models.user_models import User

class UserRepository:
    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def create_user(data):
        company_id = data.get('company')
        profile = data.get('profile')

        # Validar se a empresa existe
        if company_id:
            company = Company.objects.filter(id=company_id).first()
            if not company:
                raise ValueError("Company with the given ID does not exist")
        else:
            raise ValueError("Company is required")

        user = User.objects.create_user(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=data['password'],
            status=data['status'],
            company=company,
            profile=profile
        )
        return user

    @staticmethod
    def update_user(user_id, data):
        try:
            user = User.objects.get(id=user_id)
            for field, value in data.items():
                if hasattr(user, field):
                    setattr(user, field, value)
            user.save()
            return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def delete_user(user_id):
        user = User.objects.filter(id=user_id).first()
        if user:
            user.delete()
        return user
