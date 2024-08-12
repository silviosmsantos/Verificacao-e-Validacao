from django.urls import path
from .views import login_view, register_view, home_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login_view, name='login'),  # Página de login
    path('register/', register_view, name='register'),  # Página de registro
    path('home/', home_view, name='home'),  # Página inicial após login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Adicione esta linha
]
