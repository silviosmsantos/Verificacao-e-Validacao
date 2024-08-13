from django.urls import path
from .views import  catalog_view, login_view, messages_view, profile_view, register_view, home_view, settings_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'), 
    path('home/', home_view, name='home'),  
    path('catalog/', catalog_view, name='catalog_list'),
    path('messages/', messages_view, name='messages'),
    path('profile/', profile_view, name='profile'),
    path('settings/', settings_view, name='settings'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete')
]
