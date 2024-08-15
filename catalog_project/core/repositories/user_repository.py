from core.models.company_models import Company
from core.models.permission_models import Permission
from core.models.userPermission import UserPermission
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

        if company_id:
            company = Company.objects.filter(id=company_id).first()
            if not company:
                raise ValueError("A empresa especificada não existe.")
        else:
            raise ValueError("A empresa é obrigatoria.")

        user = User.objects.create_user(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=data['password'],
            status=data['status'],
            company=company,
            profile=profile
        )

        if profile == 'admin':
            permissions = Permission.objects.all()
            for permission in permissions:
                UserPermission.objects.create(user=user, permission=permission)

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
