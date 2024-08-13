from django.core.management.base import BaseCommand
from core.models.company_models import Company
from core.models.user_models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Create a fake user'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Criação de uma empresa fictícia
        company = Company.objects.create(name=fake.company())

        # Criação de um usuário fictício
        user = User.objects.create(
            email=fake.email(),
            phone=fake.phone_number(),
            name=fake.name(),
            status='active',
            company=company
        )
        # Definir a senha usando o método set_password
        _password = fake.password()

        user.set_password(_password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'User created: {user.email}'))
        self.stdout.write(self.style.SUCCESS(f'User senha: {_password}'))