import os
import sys
from decouple import config
from django.core.management import execute_from_command_line 

def ensure_media_directory():
    media_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
    if not os.path.exists(media_root):
        os.makedirs(media_root)
        print(f'Pasta {media_root} criada com sucesso.')

def run_management_command(command):
    execute_from_command_line(['manage.py'] + command)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalog_project.settings')
    ensure_media_directory()

    command = sys.argv[1] if len(sys.argv) > 1 else ""

    try:
        if command == 'migrate':
            print("Rodando as migrações...")
            run_management_command(['migrate', '--noinput'])
            run_management_command(['collectstatic', '--noinput'])

        execute_from_command_line(sys.argv)

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

if __name__ == '__main__':
    main()
