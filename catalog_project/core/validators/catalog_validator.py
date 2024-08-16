def validate_catalog_data(data, is_update=False):
    if not is_update:
        if 'name' not in data or not data['name']:
            raise ValueError("Catalog must have a name")
        if 'status' not in data:
            raise ValueError("Catalog must have a status")
        if 'company' not in data:
            raise ValueError("Catalog must have an associated company")
        if 'user' not in data:
            raise ValueError("Catalog must have an associated user")
    else:
        if 'name' in data and not data['name']:
            raise ValueError("Catalog name cannot be empty")
        if 'status' in data and not data['status']:
            raise ValueError("Catalog status cannot be empty")
        if 'company' in data and data['company'] is None:
            raise ValueError("Catalog must have a valid company")
        if 'user' in data and data['user'] is None:
            raise ValueError("Catalog must have a valid user")
