# core/validators/message_validator.py
def validate_message_data(data, is_update=False):
    if not is_update:
        if 'content' not in data or not data['content']:
            raise ValueError("Message must have content")
        if 'user' not in data:
            raise ValueError("Message must have an associated user")
        if 'catalog' not in data:
            raise ValueError("Message must have an associated catalog")
    else:
        if 'content' in data and not data['content']:
            raise ValueError("Message content cannot be empty")
        if 'user' in data and data['user'] is None:
            raise ValueError("Message must have a valid user")
        if 'catalog' in data and data['catalog'] is None:
            raise ValueError("Message must have a valid catalog")
