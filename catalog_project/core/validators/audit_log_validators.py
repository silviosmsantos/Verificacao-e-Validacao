def validate_audit_log_data(data):
    if 'action' not in data or data['action'] not in ['create', 'update', 'delete']:
        raise ValueError("Invalid action for audit log")
    if 'user' not in data:
        raise ValueError("Audit log must have an associated user")
