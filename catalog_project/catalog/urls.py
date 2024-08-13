from django.urls import path
from .views import catalog_view, login_view, messages_view, profile_view, register_view, home_view, settings_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login_view, name='login'),  # Página de login
    path('register/', register_view, name='register'),  # Página de registro
    path('home/', home_view, name='home'),  # Página inicial após login
    path('catalog/', catalog_view, name='catalog_list'),
    path('messages/', messages_view, name='messages'),
    path('profile/', profile_view, name='profile'),
    path('settings/', settings_view, name='settings'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Adicione esta linha
]
