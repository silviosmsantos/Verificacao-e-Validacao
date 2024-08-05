from core.repositories.audit_log_repository import AuditLogRepository

class AuditLogService:

    @staticmethod
    def create_audit_log(data):
        return AuditLogRepository.create_audit_log(data)

    @staticmethod
    def get_audit_log_by_id(audit_log_id):
        return AuditLogRepository.get_audit_log_by_id(audit_log_id)

    @staticmethod
    def get_all_audit_logs():
        return AuditLogRepository.get_all_audit_logs()

    @staticmethod
    def update_audit_log(audit_log_id, data):
        return AuditLogRepository.update_audit_log(audit_log_id, data)

    @staticmethod
    def delete_audit_log(audit_log_id):
        AuditLogRepository.delete_audit_log(audit_log_id)
