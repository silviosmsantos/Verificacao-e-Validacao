# catalog_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # URLs do admin
    path('', include('catalog.urls')),  # Inclui as URLs da aplicação catalog
]
