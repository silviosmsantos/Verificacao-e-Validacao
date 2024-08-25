import base64
import os
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class ImageSaveError(Exception):
    """Custom exception for errors during image saving."""
    pass

def save_image_from_base64(base64_image_data):
    try:
        _format, imgstr = base64_image_data.split(';base64,')
        ext = _format.split('/')[-1]
        image_file = ContentFile(base64.b64decode(imgstr), name=f"image.{ext}")
        unique_filename = f'{uuid.uuid4().hex}{os.path.splitext(image_file.name)[1]}'
        file_path = default_storage.save(f'{unique_filename}', image_file)
        image_name = os.path.basename(file_path)
        return image_name
    except Exception as e:
        raise ImageSaveError(f"Erro ao salvar a imagem: {e}")

def image_to_base64(image):
    if not image:
        return None
    try:
        image_file = image.read()
        base64_encoded = base64.b64encode(image_file).decode('utf-8')
        filename = image.name
        extension = os.path.splitext(filename)[1].lstrip('.').lower()  # Ex: 'png'
        mime_type = f'image/{extension}'
        return f"data:{mime_type};base64,{base64_encoded}"
    except Exception as e:
        print(f"Erro ao converter imagem para Base64: {e}")
        return None