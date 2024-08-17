# core/repositories/product_repository.py

from core.models.product_models import Product

class ProductRepository:
    def create_product(self, data):
        product = Product.objects.create(**data)
        return product

    def get_product(self, product_id):
        return Product.objects.filter(id=product_id).first()

    def update_product(self, product_id, data):
        product = Product.objects.filter(id=product_id).first()
        if product:
            for attr, value in data.items():
                setattr(product, attr, value)
            product.save()
        return product

    def delete_product(self, product_id):
        Product.objects.filter(id=product_id).delete()

    def list_products(self):
        return Product.objects.all()
