from core.models.audit_log_models import AuditLog
from core.validators.audit_log_validators import validate_audit_log_data

class AuditLogRepository:

    @staticmethod
    def create_audit_log(data):
        validate_audit_log_data(data)
        return AuditLog.objects.create(**data)

    @staticmethod
    def get_audit_log_by_id(audit_log_id):
        return AuditLog.objects.get(id=audit_log_id)

    @staticmethod
    def get_all_audit_logs():
        return AuditLog.objects.all()

    @staticmethod
    def update_audit_log(audit_log_id, data):
        validate_audit_log_data(data)
        audit_log = AuditLog.objects.get(id=audit_log_id)
        for key, value in data.items():
            setattr(audit_log, key, value)
        audit_log.save()
        return audit_log

    @staticmethod
    def delete_audit_log(audit_log_id):
        audit_log = AuditLog.objects.get(id=audit_log_id)
        audit_log.delete()
