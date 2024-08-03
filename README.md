## Passo a Passo para Configuração de um Projeto Django

### 1. Instalar Django:

```bash
  pip install django
```

### 2. Iniciar um projeto Django:

```bash
  django-admin startproject config .
```

### 3. Iniciar um aplicativo dentro do projeto:

```bash
- python3 manage.py startapp catalog
```

### 4. Criar um ambiente virtual:

```bash
  python -m venv venv
```

### 4. Ativar ambiente virtual:

```bash
  source venv/bin/activate
```

### 5. Criar as Migrações para os Modelos

```bash
  python3 manage.py makemigrations
```

### 6. Aplicar as Migrações ao Banco de Dados

```bash
  python3 manage.py migrate
```

### 7. Criar um superusuário:

```bash
  python3 manage.py createsuperuser
```

### 8. Rodar o servidor de desenvolvimento:

```bash
  python3 manage.py runserver
```
