from core.models.product_models import Product
from core.models.company_models import Company
from core.models.category_models import Category  # Certifique-se de que o modelo Category está importado

class ProductRepository:
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_product_by_id(product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None
        
    @staticmethod
    def create_product(data):
        if 'company' in data:
            data['company'] = Company.objects.get(id=data['company'])
        if 'category' in data:
            data['category'] = Category.objects.get(id=data['category'])
        return Product.objects.create(**data)
    
    @staticmethod
    def update_product(product_id, data):
        if 'company' in data:
            data['company'] = Company.objects.get(id=data['company'])
        if 'category' in data:
            data['category'] = Category.objects.get(id=data['category'])
        product = ProductRepository.get_product_by_id(product_id)
        if product:
            for key, value in data.items():
                setattr(product, key, value)
            product.save()
            return product
        return None

    @staticmethod
    def delete_product(product_id):
        product = ProductRepository.get_product_by_id(product_id)
        if product:
            product.delete()
            return True
        return False
