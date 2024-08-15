from django.shortcuts import render, redirect
from catalog.forms.login_form import LoginForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from catalog.forms.profile_form import ProfileForm
from catalog.forms.register_form import RegisterForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from catalog.forms.userProfiile_form import UserProfileForm
from core.models.company_models import Company
from core.models.permission_models import Permission
from core.models.userPermission import UserPermission
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
            except Exception as e:
                messages.error(request, 'Erro ao criar o usuário.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'home.html', {'user': request.user})

@login_required
def catalog_view(request):
    return render(request, 'catalog.html')

@login_required
def messages_view(request):
    return render(request, 'messages.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def list_permissions(request):
    user_permissions = UserPermission.objects.filter(user=request.user)
    
    return render(request, 'user_permission.html', {
        'permissions': user_permissions
    })


@login_required
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