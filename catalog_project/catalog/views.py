
from django.db import transaction
import json
from django.http import  JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from jsonschema import ValidationError
from catalog.forms.catalog_form import CatalogForm, ProductFormSet
from catalog.forms.categoryForm import CategoryForm
from catalog.forms.company_form import CompanyForm
from catalog.forms.login_form import LoginForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from catalog.forms.message_form import MessageFilterForm
from catalog.forms.product_form import ProductForm
from catalog.forms.profile_form import ProfileForm
from catalog.forms.register_form import RegisterForm
from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from core.helpers.ultis import image_to_base64, save_image_from_base64
from core.models.catalog_models import Catalog
from core.models.category_models import Category
from core.models.company_models import Company
from core.models.product_models import Product
from core.models.userPermission import UserPermission
from core.services.catalog_service import CatalogService
from core.services.category_service import CategoryService
from core.services.company_service import CompanyService
from core.services.message_service import MessageService
from core.services.product_services import ProductService
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

def profile_required(profiles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.profile not in profiles:
                messages.error(request, 'Você não tem permissão para acessar esta página.')
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

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
                    'status': 'active',
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

def company_register_view(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                data['status'] = 'active'
                CompanyService.create_company(data)
                messages.success(request, 'Empresa cadastrada com sucesso!')
                return redirect('login')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = CompanyForm()

    return render(request, 'company_register.html', {'form': form})

@require_http_methods(["GET"]) 
def catalog_company_visualize_product(request):
    companies = Company.objects.all()
    catalogs = None
    selected_company = None

    company_id = request.GET.get('company_id')
    if company_id:
        try:
            selected_company = get_object_or_404(Company, id=company_id)
            catalogs = CatalogService.list_catalogs_by_company(selected_company.id)
        except ValueError:
            selected_company = None
            catalogs = None

    return render(request, 'catalog_company_visualize_product.html', {
        'companies': companies,
        'catalogs': catalogs,
        'selected_company': selected_company
    })

def catalog_detail(request):
    catalog_id = request.GET.get('catalog_id')
    if catalog_id:
        catalog = CatalogService.get_catalog(catalog_id)
        if catalog is None:
            messages.error(request, 'Catálogo não encontrado.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    products = catalog.products_catalog.all()

    return render(request, 'catalog_detail.html', {
        'catalog': catalog,
        'products': products
    })

@login_required
@require_http_methods(["GET", "POST"]) 
@profile_required(profiles=['admin', 'manager']) 
def catalog_list_view(request):
    user = request.user
    company = user.company

    name = request.GET.get('name', '')
    status = request.GET.get('status', '')
    catalogs = CatalogService.list_catalogs_by_company(company.id)
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
@profile_required(profiles=['admin', 'manager']) 
def get_products_by_catalog_view(request, catalog_id):
    products = Product.objects.filter(catalog_id=catalog_id)
    product_list = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'categoryId': product.category.id if product.category else None,
            'status': product.status,
            'description': product.description,
            'imageBase64': image_to_base64(product.image) 
        }
        for product in products
    ]
    return JsonResponse({'products': product_list})

@login_required
@require_http_methods(["GET", "POST"])
@profile_required(profiles=['admin', 'manager'])
def catalog_create_view(request, catalog_id=None):
    user = request.user
    company = user.company

    if catalog_id:
        catalog = get_object_or_404(Catalog, id=catalog_id, company=company)
        messages.info(request, "Editando o catálogo existente.")
    else:
        catalog = None

    if request.method == 'POST':
        catalog_form = CatalogForm(request.POST, instance=catalog)
        if catalog_form.is_valid():
            catalog = catalog_form.save(commit=False)
            catalog.company = company
            catalog.user = user
            catalog.save()
            if catalog_id:
                messages.success(request, "Catálogo atualizado com sucesso.")
            else:
                messages.success(request, "Catálogo criado com sucesso.")
        else:
            messages.error(request, "Erro ao salvar o catálogo.")
    else:
        catalog_form = CatalogForm(instance=catalog)

    return render(request, 'catalog_create.html', {
        'catalog_form': catalog_form,
        'catalog': catalog
    })

@login_required
@require_http_methods(["GET", "POST"])
@transaction.atomic
def add_products_view(request, catalog_id):
    user = request.user
    company = user.company
    catalog = Catalog.objects.get(id=catalog_id)
    categories = CategoryService.get_categories_by_company(company.id)

    if request.method == 'POST':
        products_str = request.POST.get('product_data')
        if products_str:
            try:
                products = json.loads(products_str)
                for product_data in products:
                    product_data['catalog'] = catalog
                    category_id = product_data.get("category")
                    category = Category.objects.filter(id=category_id).first()
                    if category is None:
                        raise ValueError(f"Categoria com id {category_id} não encontrada.")
                    
                    product_data["category"] = category
                    ProductService().create_product(product_data)

                messages.success(request, "Produtos adicionados com sucesso!")
                return redirect('catalog_list')
            except Exception as e:
                messages.error(request, f"Erro ao adicionar produtos: {str(e)}")
        else:
            messages.error(request, "Nenhum produto foi adicionado.")
    else:
        formset = ProductFormSet(queryset=Product.objects.none(), form_kwargs={'categories': categories})

    return render(request, 'add_products.html', {
        'catalog': catalog,
        'formset': formset,
        'categories': categories,
    })

@login_required
@require_http_methods(["POST"])
@transaction.atomic
def save_products_view(request, catalog_id):
    try:
        catalog = get_catalog_or_404(catalog_id)
        product_data_list = load_product_data_from_request(request)
        remove_existing_products_and_images(catalog)
        add_new_products(product_data_list, catalog)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': f"Erro ao processar a solicitação: {str(e)}"}, status=500)

def get_catalog_or_404(catalog_id):
    try:
        return CatalogService.get_catalog(catalog_id)
    except Catalog.DoesNotExist:
        raise JsonResponse({'error': 'Catálogo não encontrado'}, status=404)

def load_product_data_from_request(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        return data.get('product_data', [])
    except json.JSONDecodeError:
        raise JsonResponse({'error': 'Formato dos dados incorretos'}, status=400)

def remove_existing_products_and_images(catalog):
    existing_products = Product.objects.filter(catalog=catalog)
    for product in existing_products:
        if product.image:
            delete_image_if_exists(product.image.name)
        product.delete()

def delete_image_if_exists(image_path):
    if default_storage.exists(image_path):
        default_storage.delete(image_path)

def add_new_products(product_data_list, catalog):
    for product_data in product_data_list:
        category = get_category_or_404(product_data['category'])
        process_product_data(product_data, category, catalog)

def get_category_or_404(category_id):
    try:
        return CategoryService().get_category_by_id(category_id)
    except Category.DoesNotExist:
        raise JsonResponse({'error': 'Categoria não encontrada'}, status=404)

def process_product_data(product_data, category, catalog):
    if 'image' in product_data and product_data['image']:
        product_data['image'] = save_image_from_base64(product_data['image'])
    
    product_data['category'] = category
    product_data['catalog'] = catalog

    ProductService().create_product(product_data)

@login_required
@require_http_methods(["GET", "POST"])
@profile_required(profiles=['admin', 'manager']) 
def catalog_delete_view(request, pk):
    try:
        catalog = get_object_or_404(Catalog, id=pk)
    except ValueError:
        messages.error(request, 'Catálogo não encontrado. O valor fornecido não é um UUID válido.')
        return redirect('catalog_list')

    if request.method == 'POST':
        CatalogService.delete_catalog(catalog.id)
        messages.success(request, 'Catálogo excluído com sucesso!')
        return redirect('catalog_list')

    return render(request, 'catalog_delete.html', {'catalog': catalog})

@login_required
@require_http_methods(["GET"])
@profile_required(profiles=['admin', 'manager']) 
def home_view(request):
    user = request.user
    company = user.company

    catalog_count = CatalogService.list_catalogs_by_company(company.id).count()
    category_count = CategoryService.get_categories_by_company(company.id).count()
    message_count = MessageService.list_messages_by_company(company.id).count()

    context = {
        'user': user.name,
        'catalog_count': catalog_count,
        'category_count': category_count,
        'message_count': message_count,
    }
    return render(request, 'home.html', context)

@login_required
@require_http_methods(["GET"])
@profile_required(profiles=['admin', 'manager']) 
def category_list_by_company_view(request):
    user_company = request.user.company
    name_filter = request.GET.get('name', '').strip()
    status_filter = request.GET.get('status', '').strip()
    categories = CategoryService.get_categories_by_company(user_company.id)
    if name_filter:
        categories = categories.filter(name__icontains=name_filter)
    if status_filter:
        categories = categories.filter(status=status_filter)
    context = {
        'categories': categories,
        'name_filter': name_filter,
        'status_filter': status_filter,
    }
    return render(request, 'category_company_list.html', context)

@login_required
@require_http_methods(["GET", "POST"])
@profile_required(profiles=['admin', 'manager']) 
def category_delete_view(request, pk):
    category = CategoryService.get_category_by_id(pk)
    if not category:
        messages.error(request, 'Category não encontrada.')
        return redirect('categories_by_company')
    if request.method == "POST":
        CategoryService.delete_category(pk)
        messages.success(request, 'category excluída com sucesso.')
        return redirect('categories_by_company')
    return render(request, 'category_delete.html', {'category': category})

@login_required
@require_http_methods(["GET", "POST"])
@profile_required(profiles=['admin', 'manager']) 
def category_create_view(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            company = request.user.company
            data = form.cleaned_data
            data['company'] = company.id
            CategoryService.create_category(data)
            messages.success(request, 'Categoria criada com sucesso.')
            return redirect('categories_by_company') 
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form, 'action': 'Criar'})

@login_required
@require_http_methods(["GET", "POST"])
@profile_required(profiles=['admin', 'manager']) 
def category_edit_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            data = form.cleaned_data
            data['company'] = category.company.id
            CategoryService.update_category(category.id, data)
            messages.success(request, 'Categoria atualizada com sucesso.')
            return redirect('categories_by_company')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'category_form.html', {'form': form, 'action': 'Editar'})

@login_required
@require_http_methods(["GET"]) 
@profile_required(profiles=['admin', 'manager']) 
def messages_list_view(request):
    user = request.user
    company = user.company

    form = MessageFilterForm(request.GET or None)
    messages = MessageService.list_messages_by_company(company.id)
    
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
@require_http_methods(["GET", "POST"])
@profile_required(profiles=['admin', 'manager'])
def message_delete_view(request, message_id):
    message = MessageService.get_message(message_id)
    if not message:
        messages.error(request, 'Mensagem não encontrada.')
        return redirect('messages_list')
    if request.method == 'POST':
        MessageService.delete_message(message_id)
        messages.success(request, 'Mensagem excluída com sucesso.')
        return redirect('messages_list')
    return render(request, 'messages_delete.html', {'message': message})

@login_required
@require_http_methods(["GET"]) 
@profile_required(profiles=['admin']) 
def permissions_list_view(request):
    user_permissions = UserPermission.objects.filter(user=request.user)
    return render(request, 'permission_list.html', {
        'permissions': user_permissions
    })

@login_required
@require_http_methods(["GET", "POST"]) 
@profile_required(profiles=['admin']) 
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            data = form.cleaned_data
            company = user.company 
            data_to_update = {
                'name': data.get('name'),
                'phone': data.get('phone'),
                'email': user.email,
                'status': user.status,
                'profile': user.profile,
                'company': company
            }
            UserService.update_user(user.id, data_to_update)
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form})
