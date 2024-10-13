from django.test import TestCase
from core.models.user_models import User
from core.models.audit_log_models import AuditLog
from core.services.audit_log_service import AuditLogService
from core.models.company_models import Company

class AuditLogServiceTest(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name='Test Company', status='active')
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            phone="123456789",
            password="password",
            status='active',
            company=self.company, 
            profile='manager'
        )
        self.audit_log_data = {
            'action': 'create',
            'user': self.user
        }

    def test_create_audit_log(self):
        audit_log = AuditLogService.create_audit_log(self.audit_log_data)
        self.assertEqual(audit_log.action, 'create')
        self.assertEqual(audit_log.user, self.user)

    def test_get_audit_log_by_id(self):
        audit_log = AuditLogService.create_audit_log(self.audit_log_data)
        fetched_log = AuditLogService.get_audit_log_by_id(audit_log.id)
        self.assertEqual(fetched_log, audit_log)

    def test_get_all_audit_logs(self):
        AuditLogService.create_audit_log(self.audit_log_data)
        logs = AuditLogService.get_all_audit_logs()
        self.assertEqual(len(logs), 1)

    def test_update_audit_log(self):
        audit_log = AuditLogService.create_audit_log(self.audit_log_data)
        updated_data = {'action': 'update', 'user': self.user}
        updated_log = AuditLogService.update_audit_log(audit_log.id, updated_data)
        self.assertEqual(updated_log.action, 'update')
        self.assertEqual(updated_log.user, self.user)

    def test_delete_audit_log(self):
        audit_log = AuditLogService.create_audit_log(self.audit_log_data)
        AuditLogService.delete_audit_log(audit_log.id)
        with self.assertRaises(AuditLog.DoesNotExist):
            AuditLogService.get_audit_log_by_id(audit_log.id)

    def test_create_audit_log_invalid_action(self):
        invalid_data = {'action': 'invalid', 'user': self.user}
        with self.assertRaises(ValueError):
            AuditLogService.create_audit_log(invalid_data)

    def test_create_audit_log_missing_user(self):
        invalid_data = {'action': 'create'}
        with self.assertRaises(ValueError):
            AuditLogService.create_audit_log(invalid_data)
