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
    existing_companies = Company.objects.all().count()
    if existing_companies == 0:
        for _ in range(5):
            company, created = Company.objects.get_or_create(
                name=fake.company(),
                defaults={'status': random.choice(['active', 'inactive'])}
            )
            companies.append(company)
    else:
        companies = Company.objects.all()
    return companies

def create_users(companies):
    users = []
    existing_users = User.objects.all().count()
    if existing_users == 0:
        for _ in range(10):
            user, created = User.objects.get_or_create(
                email=fake.email(),
                defaults={
                    'name': fake.name(),
                    'phone': fake.phone_number(),
                    'status': 'active',
                    'company': random.choice(companies)  
                }
            )
            if created:
                user.set_password('@123456') 
                user.save()
            users.append(user)
    else:
        users = User.objects.all()
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
