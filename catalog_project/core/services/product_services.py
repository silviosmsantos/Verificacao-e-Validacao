from core.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def create_product(self, data):
        return self.repository.create_product(data)

    def get_product(self, product_id):
        return self.repository.get_product(product_id)

    def update_product(self, product_id, data):
        return self.repository.update_product(product_id, data)

    def delete_product(self, product_id):
        self.repository.delete_product(product_id)

    def list_products(self):
        return self.repository.list_products()
