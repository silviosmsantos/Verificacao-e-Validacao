from core.models.category_models import Category
from core.models.company_models import Company

class CategoryRepository:
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_category_by_id(category_id):
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None

    @staticmethod
    def get_categories_by_company(company_id):
        try:
            company = Company.objects.get(id=company_id)
            return Category.objects.filter(company=company.pk)
        except Company.DoesNotExist:
            return None

    @staticmethod
    def create_category(data):
        if 'company' in data:
            data['company'] = Company.objects.get(id=data['company'])
        return Category.objects.create(**data)

    @staticmethod
    def update_category(category_id, data):
        if 'company' in data:
            data['company'] = Company.objects.get(id=data['company'])
        category = CategoryRepository.get_category_by_id(category_id)
        if category:
            for key, value in data.items():
                setattr(category, key, value)
            category.save()
            return category
        return None

    @staticmethod
    def delete_category(category_id):
        category = CategoryRepository.get_category_by_id(category_id)
        if category:
            category.delete()
            return True
        return False
