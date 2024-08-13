from django.core.management.base import BaseCommand
from core.models.company_models import Company
from core.models.user_models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Create a fake user with a specific email if it does not already exist'

    def handle(self, *args, **kwargs):
        fake = Faker()
        email = fake.email

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'User with email {email} already exists.'))
        else:
            # Cria uma nova empresa fictícia
            company = Company.objects.create(name=fake.company())
            
            # Cria um novo usuário
            user = User.objects.create(
                email=email,
                phone=fake.phone_number(),
                name=fake.name(),
                status='active',
                company=company
            )
            user.set_password(fake.password)
            user.save()

