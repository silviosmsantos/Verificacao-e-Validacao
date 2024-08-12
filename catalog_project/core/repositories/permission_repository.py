from .permission_repository import Permission
from .user_repository import User

class PermissionRepository:
    @staticmethod
    def get_all_permission():
        return Permission.objects.all()

    @staticmethod
    def get_permission_by_id(permission_id):
        return Permission.objects.filter(id=permission_id).first()

    @staticmethod
    def create_permission(data):
        if 'user' in data:
            data['user'] = User.objects.get(id=data['user'])
        return Permission.objects.create(**data)


    @staticmethod
    def update_permission(permission_id, data):
        permission = Permission.objects.filter(id=permission_id).first()
        if permission:
            for key, value in data.items():
                setattr(permission, key, value)
            permission.save()
        return permission

    @staticmethod
    def delete_permission(permission_id):
        permission = Permission.objects.filter(id=permission_id).first()
        if permission:
            permission.delete()
        return permission
    

    
