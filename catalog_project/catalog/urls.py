from django.urls import path
from .views import  catalog_create_view, catalog_delete_view, catalog_list_view, message_delete_view, permissions_list_view, login_view, messages_list_view, product_create_view, profile_view, register_view, home_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'), 
    path('home/', home_view, name='home'),  
    path('catalog_list/', catalog_list_view, name='catalog_list'),
    path('catalog_create/', catalog_create_view, name='catalog_create'),
    path('catalogs/delete/<uuid:pk>/', catalog_delete_view, name='catalog_delete'),
    path('product_create/', product_create_view, name='product_create'),
    path('messages_list/', messages_list_view, name='messages_list'),
    path('message_delete/<uuid:message_id>/', message_delete_view, name='message_delete'),
    path('profile/', profile_view, name='profile'),
    path('permissions_list/', permissions_list_view, name='permissions_list'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete')
]
