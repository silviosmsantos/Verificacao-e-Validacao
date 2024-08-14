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
        # Verifica se company_id está presente e é um número
        company_id = data.get('company')
        if company_id:
            company = Company.objects.filter(id=company_id).first()  # Obtém a instância da empresa
            if not company:
                raise ValueError("Company with the given ID does not exist")
        else:
            company = None

        user = User.objects.create_user(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=data['password'],
            status=data['status'],
            company=company
        )
        return user

    @staticmethod
    def update_user(user_id, data):
        user = User.objects.filter(id=user_id).first()
        if user:
            # Atualiza apenas os campos permitidos
            allowed_fields = ['name', 'phone', 'status']
            for attr, value in data.items():
                if attr in allowed_fields:
                    setattr(user, attr, value)
            user.save()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.objects.filter(id=user_id).first()
        if user:
            user.delete()
        return user
