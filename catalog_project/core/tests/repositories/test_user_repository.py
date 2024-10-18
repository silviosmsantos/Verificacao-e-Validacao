from core.models.userPermission_models import UserPermission
from core.repositories.user_repository import UserRepository
from core.models.user_models import User
from core.models.company_models import Company
from core.models.permission_models import Permission
from ..base_test_case import BaseTestCase

class UserRepositoryTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.permission1 = Permission.objects.create(name='Permission 1', status='active')
        self.permission2 = Permission.objects.create(name='Permission 2', status='active')

    def test_get_all_users(self):
        users = UserRepository.get_all_users()
        self.assertIn(self.user, users)

    def test_get_user_by_id(self):
        user = UserRepository.get_user_by_id(self.user.id)
        self.assertEqual(self.user, user)

    def test_get_users_by_company_only_admin(self):
        users = UserRepository.get_users_by_company(self.company.id)
        self.assertIn('testuser123@example.com', users.values_list('email', flat=True))

    def test_create_user(self):
        data = {
            'name': 'New User',
            'email': 'new@example.com',
            'phone': '0987654321',
            'password': 'newpassword',
            'status': 'active',
            'company': self.company.id,
            'profile': 'admin' 
        }
        user = UserRepository.create_user(data)
        self.assertEqual(user.name, 'New User')
        self.assertEqual(user.company, self.company)
        self.assertEqual(user.profile, 'admin')
        self.assertTrue(user.check_password('newpassword'))
        user_permissions = UserPermission.objects.filter(user=user)
        self.assertEqual(user_permissions.count(), 5)
        self.assertIn(self.permission1, [up.permission for up in user_permissions])
        self.assertIn(self.permission2, [up.permission for up in user_permissions])

    def test_update_user(self):
        data = {
            'name': 'Updated User',
            'email': 'updated@example.com',
            'profile': 'admin'
        }
        user = UserRepository.update_user(self.user.id, data)
        self.assertEqual(user.name, 'Updated User')
        self.assertEqual(user.email, 'updated@example.com')
        self.assertEqual(user.profile, 'admin')
        self.assertEqual(user.company, self.company)

    def test_delete_user(self):
        UserRepository.delete_user(self.user.id)
        user = UserRepository.get_user_by_id(self.user.id)
        self.assertIsNone(user)