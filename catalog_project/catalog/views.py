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
from core.services.user_service import UserService

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
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        company_name = form.cleaned_data.get('company')
        if company_name:
            company = Company.objects.filter(name=company_name).first()
            if not company:
                return render(request, 'register.html', {'form': form, 'error': 'Company does not exist'})
        else:
            company = None
        try:
            user_data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'password': form.cleaned_data['password'],
                'status': form.cleaned_data['status'],
                'company': company.pk if company else None
            }
            UserService.create_user(user_data)
            return redirect('login')
        except Exception as e:
            return render(request, 'register.html', {'form': form, 'error': 'Error creating user'})
    
    return render(request, 'register.html', {'form': form})



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
def settings_view(request):
    return render(request, 'settings.html')

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data_to_update = {
                'name': data.get('name'),
                'phone': data.get('phone'),
                'status': data.get('status')
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
            'company': user.company
        }
        form = ProfileForm(initial=initial_data)

    return render(request, 'profile.html', {'form': form})
