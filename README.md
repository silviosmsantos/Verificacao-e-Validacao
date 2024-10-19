## Step-by-step guide to set up the project

Please ensure you have **Python 3.10.12** installed before running the project.

You can verify your Python version by running the following command:

```bash
  python --version
```

### 1. Create a Virtual Environment:

```bash
  python -m venv venv
```

### 2. Activate the Virtual Environment:

```bash
  source venv/bin/activate
```

### 3. Install Dependencies from requirements.txt:

```bash
  pip install -r requirements.txt
```

### 4. Create Migrations for the Models:

```bash
  python manage.py makemigrations
```

### 5. Apply Migrations to the Database:

```bash
  python manage.py migrate
```

### 6. Run the Development Server:

```bash
  python manage.py runserver
```

### 7. Run docs class project

To generate and view the class documentation:

1. Navigate to the `docs/` folder:

   ```bash
   cd docs/
   ```

2. Generate the HTML documentation:

```bash
  make html
```

3. Open the generated documentation in your browser by accessing:

```bash
  open _build/html/index.html
```

### 8. Run tests application

To run the tests and view the test coverage report:

1. Run the tests using `pytest` and generate the coverage report:

```bash
  pytest
```

2. After the tests have run, open the coverage report in your browser:

```bash
open htmlcov/index.html
```
