def validate_audit_log_data(data):
    if 'action' not in data or data['action'] not in ['create', 'update', 'delete']:
        raise ValueError("Ação inválida para o log de auditoria")
    if 'user' not in data:
        raise ValueError("O log de auditoria deve ter um usuário associado")
