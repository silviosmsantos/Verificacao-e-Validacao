from core.repositories.permission_repository import PermissionRepository

class PermissionService:
    @staticmethod
    def get_all_permissions():
        return PermissionRepository.get_all_companies()

    @staticmethod
    def get_permission_by_id(permission_id):
        return PermissionRepository.get_permission_by_id(permission_id)

    @staticmethod
    def create_permission(data):
        return PermissionRepository.create_permission(data)

    @staticmethod
    def update_permission(permission_id, data):
        return PermissionRepository.update_permission(permission_id, data)

    @staticmethod
    def delete_permission(permission_id):
        return PermissionRepository.delete_permission(permission_id)
