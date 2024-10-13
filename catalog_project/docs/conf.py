import os
import sys

# Ajusta o caminho para o diretório do seu projeto
sys.path.insert(0, os.path.abspath('..'))  # Modifique se necessário

# Define a variável de ambiente DJANGO_SETTINGS_MODULE
os.environ['DJANGO_SETTINGS_MODULE'] = 'catalog_project.settings'  # Ajuste conforme o nome do seu projeto

import django
django.setup()  # Inicializa o Django

# -- Project information -----------------------------------------------------
project = 'catalog_project'
copyright = '2024, Allyson, Caio, Cleanio, Silvio, Marcelo e Marcos.'
author = 'Allyson, Caio, Cleanio, Silvio, Marcelo e Marcos.'
release = '2024'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',  # Para importar docstrings automaticamente
    'sphinx.ext.viewcode',  # Para mostrar o código-fonte nos documentos
    'sphinx_autodoc_typehints',  # Para incluir anotações de tipo
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'pt-br'

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
