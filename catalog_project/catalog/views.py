from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from catalog.forms.catalog_form import CatalogForm
from catalog.forms.login_form import LoginForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from catalog.forms.message_form import MessageFilterForm
from catalog.forms.product_form import ProductForm
from catalog.forms.profile_form import ProfileForm
from catalog.forms.register_form import RegisterForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from core.models.catalog_models import Catalog
from core.models.message_models import Message
from core.models.userPermission import UserPermission
from core.services.catalog_service import CatalogService
from core.services.category_service import CategoryService
from core.services.message_service import MessageService
from core.services.user_service import UserService

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'catalog/reset_password_done.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'catalog/reset_password.html'
    email_template_name = 'catalog/reset_password_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'catalog/reset_password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'catalog/reset_password_complete.html'

@require_http_methods(["GET", "POST"]) 
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.email}')
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@require_http_methods(["GET", "POST"]) 
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data.get('company')
            profile = form.cleaned_data.get('profile')

            try:
                user_data = {
                    'name': form.cleaned_data['name'],
                    'email': form.cleaned_data['email'],
                    'phone': form.cleaned_data['phone'],
                    'password': form.cleaned_data['password'],
                    'status': form.cleaned_data['status'],
                    'company': company.pk, 
                    'profile': profile
                }
                UserService.create_user(user_data)
                messages.success(request, 'Usuário criado com sucesso!')
                return redirect('login')
            except Exception:
                messages.error(request, 'Erro ao criar o usuário.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
@require_http_methods(["GET"]) 
def home_view(request):
    return render(request, 'home.html', {'user': request.user})

# view do catalogo
@login_required
@require_http_methods(["GET", "POST"]) 
def catalog_list_view(request):
    name = request.GET.get('name', '')
    status = request.GET.get('status', '')
    catalogs = CatalogService.list_all_catalogs()
    if name:
        catalogs = catalogs.filter(name__icontains=name)
    if status:
        catalogs = catalogs.filter(status=status)
    context = {
        'catalogs': catalogs
    }
    return render(request, 'catalog_list.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def catalog_create_view(request):
    if request.method == 'POST':
        form = CatalogForm(request.POST)
        if form.is_valid():
            catalog_data = form.cleaned_data
            catalog_data['user'] = request.user
            catalog_data['company'] = request.user.company
            try:
                CatalogService.create_catalog(catalog_data)
                messages.success(request, 'Catálogo criado com sucesso!')
                return redirect('catalog_list')
            except ValueError as e:
                messages.error(request, f'Erro ao criar o catálogo: {e}')
                return HttpResponseBadRequest(f'Erro: {e}')
    else:
        form = CatalogForm()

    return render(request, 'catalog_create.html', {'form': form})

@login_required
@require_http_methods(["GET", "POST"])
def catalog_delete_view(request, pk):
    try:
        catalog = get_object_or_404(Catalog, id=pk)  # Usa o UUID como id
    except ValueError:
        messages.error(request, 'Catálogo não encontrado. O valor fornecido não é um UUID válido.')
        return redirect('catalog_list')

    if request.method == 'POST':
        CatalogService.delete_catalog(catalog.id)
        messages.success(request, 'Catálogo excluído com sucesso!')
        return redirect('catalog_list')

    return render(request, 'catalog_delete.html', {'catalog': catalog})


# view de messages
@login_required
@require_http_methods(["GET"]) 
def messages_list_view(request):
    form = MessageFilterForm(request.GET or None)
    messages = MessageService.list_all_messages()
    
    if form.is_valid():
        nome = form.cleaned_data.get('nome')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        sent_at = form.cleaned_data.get('sent_at')
        if nome:
            messages = messages.filter(name__icontains=nome)
        if email:
            messages = messages.filter(email__icontains=email)
        if phone:
            messages = messages.filter(phone__icontains=phone)
        if sent_at:
            messages = messages.filter(sent_at__date=sent_at)
    
    return render(request, 'messages_list.html', {'messages': messages, 'form': form})

@login_required
@require_http_methods(["GET"]) 
def permissions_list_view(request):
    user_permissions = UserPermission.objects.filter(user=request.user)
    return render(request, 'permission_list.html', {
        'permissions': user_permissions
    })

@login_required
@require_http_methods(["GET", "POST"]) 
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, user=user)
        if form.is_valid():
            data = form.cleaned_data
            data_to_update = {
                'name': data.get('name'),
                'phone': data.get('phone'),
                'status': data.get('status'),
                'profile': data.get('profile')
            }
            UserService.update_user(user.id, data_to_update)
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        initial_data = {
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'status': user.status,
            'company': user.company,
            'profile': user.profile  
        }
        form = ProfileForm(initial=initial_data, user=user)

    return render(request, 'profile.html', {'form': form})

@csrf_exempt
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return JsonResponse({
                'success': True,
                'product': {
                    'name': product.name,
                    'price': product.price,
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})