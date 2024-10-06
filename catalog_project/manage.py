import os
import sys
from decouple import config

def ensure_media_directory():
    ENVIRONMENT = config('ENVIRONMENT', default='development')
    if ENVIRONMENT != 'production':
        media_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
        if not os.path.exists(media_root):
            os.makedirs(media_root)
            print(f'Pasta {media_root} criada com sucesso.')

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalog_project.settings')
    ensure_media_directory()
    
    collectstatic_command = ['manage.py', 'collectstatic', '--noinput']
    sys.argv = collectstatic_command 

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execute_from_command_line(sys.argv)  # Executa o comando collectstatic

if __name__ == '__main__':
    main()
