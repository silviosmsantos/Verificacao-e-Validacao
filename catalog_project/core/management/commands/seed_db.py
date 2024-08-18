from django.core.management.base import BaseCommand
from faker import Faker
import secrets
from core.models.company_models import Company
from core.models.permission_models import Permission
from core.models.userPermission import UserPermission
from core.models.user_models import User
from core.models.catalog_models import Catalog
from core.models.message_models import Message
from core.models.category_models import Category
from core.models.product_models import Product

fake = Faker('pt_BR')
secure_random = secrets.SystemRandom()

class Command(BaseCommand):
    help = 'Seed the database with companies, users, permissions, catalogs, messages, and products, and assign permissions to users'

    def handle(self, *args, **kwargs):
        companies = create_companies()
        users = create_users(companies)
        permissions = create_permissions()
        assign_permissions_to_users(users, permissions)
        catalogs = create_catalogs(users, companies)
        create_categories(companies)
        create_products(catalogs)
        create_messages(catalogs)
        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))

def create_companies():
    companies = []
    for _ in range(5):
        company_name = fake.company()
        company, _ = Company.objects.get_or_create(
            name=company_name,
            defaults={'status': secure_random.choice(['active', 'inactive'])}
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
                'company': secure_random.choice(companies),
                'profile': secure_random.choice(['manager', 'admin', 'user'])
            }
        )
        if created:
            user.set_password('@123456')
            user.save()
        users.append(user)
    return users

def create_permissions():
    permissions = []
    permission_names = ['Criar', 'Atualizar', 'Deletar']
    for name in permission_names:
        permission, _ = Permission.objects.get_or_create(name=name)
        permissions.append(permission)
    return permissions

def assign_permissions_to_users(users, permissions):
    for user in users:
        for permission in permissions:
            UserPermission.objects.get_or_create(
                user=user,
                permission=permission
            )

def create_categories(companies):
    categories = []
    for company in companies:
        for _ in range(5):
            category_name = fake.word()
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={
                    'status': secure_random.choice(['active', 'inactive']),
                    'company': company
                }
            )
            categories.append(category)
    return categories

def create_catalogs(users, companies):
    catalogs = []
    for _ in range(10):
        catalog_name = fake.word()
        catalog, _ = Catalog.objects.get_or_create(
            name=catalog_name,
            defaults={
                'status': secure_random.choice(['active', 'inactive']),
                'company': secure_random.choice(companies),
                'user': secure_random.choice(users)
            }
        )
        catalogs.append(catalog)
    return catalogs

def create_products(catalogs):
    categories = Category.objects.all()
    for _ in range(20):
        product_data = {
            'name': fake.word(),
            'description': fake.text(max_nb_chars=200),
            'price': round(secure_random.uniform(10.0, 1000.0), 2),
            'image': fake.image_url(),
            'status': secure_random.choice(['active', 'inactive']),
            'category': secure_random.choice(categories),
            'catalog': secure_random.choice(catalogs)
        }
        Product.objects.create(**product_data)

def create_messages(catalogs):
    for _ in range(20):
        message_content = fake.text(max_nb_chars=200)
        Message.objects.create(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            content=message_content,
            catalog=secure_random.choice(catalogs)
        )
