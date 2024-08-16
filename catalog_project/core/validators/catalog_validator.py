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
        validate_presence('name', "Catalog must have a name")
        validate_presence('status', "Catalog must have a status")
        validate_presence('company', "Catalog must have an associated company")
        validate_presence('user', "Catalog must have an associated user")
    else:
        validate_non_empty('name', "Catalog name cannot be empty")
        validate_non_empty('status', "Catalog status cannot be empty")
        validate_non_none('company', "Catalog must have a valid company")
        validate_non_none('user', "Catalog must have a valid user")
