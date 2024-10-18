from core.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def create_user(data):
        return UserRepository.create_user(data)

    @staticmethod
    def update_user(user_id, data):
        return UserRepository.update_user(user_id, data)

    @staticmethod
    def delete_user(user_id):
        return UserRepository.delete_user(user_id)

    @staticmethod
    def list_users_by_company(company_id):
        return UserRepository.get_users_by_company(company_id)