## Passo a Passo para Configuração de um Projeto Django

### 1. Install Django:

```bash
  pip install django
```

### 2. Start a Django Project:

```bash
  django-admin startproject config .
```

### 3. Start an Application within the Project:

```bash
- python3 manage.py startapp catalog
```

### 4. Create a Virtual Environment:

```bash
  python -m venv venv
```

### 5. Activate the Virtual Environment:

```bash
  source venv/bin/activate
```

### 6. Install Dependencies from requirements.txt:

```bash
  source pip install -r requirements.txt
```

### 7. Create Migrations for the Models:

```bash
  python3 manage.py makemigrations
```

### 8. Apply Migrations to the Database:

```bash
  python3 manage.py migrate
```

### 9. Create a Superuser:

```bash
  python3 manage.py createsuperuser
```

### 10. Run the Development Server:

```bash
  python3 manage.py runserver
```
