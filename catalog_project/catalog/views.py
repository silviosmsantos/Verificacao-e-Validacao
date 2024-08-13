# catalog/views.py
from django.shortcuts import render, redirect
from catalog.forms.login_form import LoginForm
from catalog.forms.register_form import RegisterForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Certifique-se de usar a função 'login' do Django
            messages.success(request, f'Bem-vindo(a), {user.email}')
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    # Supondo que você tenha um formulário de registro
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})

@login_required
def home_view(request):
    print(request.user)
    return render(request, 'home.html', {'user': request.user})

def catalog_view(request):
    return render(request, 'catalog.html')

def messages_view(request):
    return render(request, 'messages.html')

def profile_view(request):
    return render(request, 'profile.html')

def settings_view(request):
    return render(request, 'settings.html')