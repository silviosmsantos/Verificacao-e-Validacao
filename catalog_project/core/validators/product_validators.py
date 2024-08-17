from django.core.exceptions import ValidationError

def validate_name(value):
    if len(value) < 3:
        raise ValidationError('O nome deve ter pelo menos 3 caracteres.')

def validate_description(value):
    if not value or len(value.strip()) < 10:
        raise ValidationError('A descrição deve ter pelo menos 10 caracteres e não pode ser vazia.')
    
def validate_image(value):
    if value is None:
        raise ValidationError('A imagem não pode ser vazia.')