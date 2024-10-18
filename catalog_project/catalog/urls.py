from django.urls import path
from .views import  add_products_view, catalog_company_visualize_product, catalog_create_view, catalog_delete_view, catalog_detail, catalog_list_view, category_create_view, category_delete_view, category_edit_view, category_list_by_company_view, company_register_view, get_products_by_catalog_view, message_delete_view, permissions_list_view, login_view, messages_list_view, profile_view, register_view, home_view, save_products_view, send_message_view, user_delete_view, user_list_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'), 
    path('home/', home_view, name='home'),  
    
    path('catalog_list/', catalog_list_view, name='catalog_list'),
    path('catalog_create/', catalog_create_view, name='catalog_create'),
    path('catalogs/delete/<uuid:pk>/', catalog_delete_view, name='catalog_delete'),
    path('add_products/<uuid:catalog_id>/', add_products_view, name='add_products'),
    path('catalog_visualize/', catalog_company_visualize_product, name='catalog_company_visualize_product'),
    path('catalog/edit/<uuid:catalog_id>/', catalog_create_view, name='catalog_edit'), 
    path('catalog_detail/', catalog_detail, name='catalog_detail'),
    path('catalog/<uuid:catalog_id>/save-products/', save_products_view, name='save_products'),
    path('catalog/<uuid:catalog_id>/products/', get_products_by_catalog_view, name='get_products_by_catalog'),

    path('send-message/', send_message_view, name='send_message'),

    path('categories/company/', category_list_by_company_view, name='categories_by_company'),
    path('category/create/', category_create_view, name='category_create'),
    path('category/edit/<uuid:pk>/', category_edit_view, name='category_edit'),
    path('category/delete/<uuid:pk>/', category_delete_view, name='category_delete'),

    path('company_register/', company_register_view, name='company_register'),

    path('messages_list/', messages_list_view, name='messages_list'),
    path('message_delete/<uuid:message_id>/', message_delete_view, name='message_delete'),

    path('profile/', profile_view, name='profile'),

    path('permissions_list/', permissions_list_view, name='permissions_list'),

    path('user_list_company', user_list_view, name='user_list_company'),
    path('user/delete/<uuid:pk>/', user_delete_view, name='user_delete'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete')
]
