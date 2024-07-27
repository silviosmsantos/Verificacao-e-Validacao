Criar um ambiente virtual:

- python -m venv venv
- source venv/bin/activate # No Windows use: venv\Scripts\activate

Instalar Django:

- pip install django

Iniciar um projeto Django:

- django-admin startproject config .

Iniciar um aplicativo dentro do projeto:

- python3 manage.py startapp catalog

Criar as Migrações para os Modelos

- python3 manage.py makemigrations

Aplicar as Migrações ao Banco de Dados

- python3 manage.py migrate

Criar um superusuário:

- python3 manage.py createsuperuser

Rodar o servidor de desenvolvimento:

- python3 manage.py runserver
