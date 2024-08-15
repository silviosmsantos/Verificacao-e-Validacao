from django.core.management.base import BaseCommand
from faker import Faker
import random

from core.models.company_models import Company
from core.models.permission_models import Permission
from core.models.userPermission import UserPermission
from core.models.user_models import User

fake = Faker('pt_BR')

class Command(BaseCommand):
    help = 'Seed the database with companies, users, permissions, and assign permissions to users'

    def handle(self, *args, **kwargs):
        companies = create_companies()
        users = create_users(companies)
        permissions = create_permissions()
        assign_permissions_to_users(users, permissions)
        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))

def create_companies():
    companies = []
    for _ in range(5):
        company_name = fake.company()
        company, created = Company.objects.get_or_create(
            name=company_name,
            defaults={'status': random.choice(['active', 'inactive'])}
        )
        companies.append(company)
    return companies

def create_users(companies):
    users = []
    for _ in range(10):
        email = fake.email()
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'name': fake.name(),
                'phone': fake.phone_number(),
                'status': 'active',
                'company': random.choice(companies)
            }
        )
        if created:
            user.set_password('@123456')  # Define uma senha padrão
            user.save()
        users.append(user)
    return users

def create_permissions():
    permissions = []
    permission_names = ['Criar', 'Atualizar', 'Deletar']
    for name in permission_names:
        permission, created = Permission.objects.get_or_create(name=name)
        permissions.append(permission)
    return permissions

def assign_permissions_to_users(users, permissions):
    for user in users:
        for permission in permissions:
            UserPermission.objects.get_or_create(
                user=user,
                permission=permission
            )
