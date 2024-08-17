def validate_catalog_data(data, is_update=False):
    def validate_presence(key, message):
        if key not in data:
            raise ValueError(message)
    
    def validate_non_empty(key, message):
        if data.get(key) in [None, '']:
            raise ValueError(message)
    
    def validate_non_none(key, message):
        if data.get(key) is None:
            raise ValueError(message)
    
    if not is_update:
        validate_presence('name', "O catálogo deve ter um nome")
        validate_presence('status', "O catálogo deve ter um status")
        validate_presence('company', "O catálogo deve estar associado a uma empresa")
        validate_presence('user', "O catálogo deve ter um usuário associado")
    else:
        validate_non_empty('name', "O nome do catálogo não pode estar vazio")
        if 'status' in data:
            validate_non_empty('status', "O status do catálogo não pode estar vazio")
        validate_non_none('company', "O catálogo deve ter uma empresa válida")
        validate_non_none('user', "O catálogo deve ter um usuário válido")
