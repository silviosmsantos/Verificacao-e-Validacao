from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Gerenciador personalizado para o modelo de usuário.

    Métodos:
        create_user(email, password=None, **extra_fields):
            Cria e retorna um usuário com o e-mail e senha fornecidos.
        
        create_superuser(email, password=None, **extra_fields):
            Cria e retorna um superusuário com o e-mail e senha fornecidos.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
