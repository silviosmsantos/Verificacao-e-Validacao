from core.repositories.category_repository import CategoryRepository

class CategoryService:
    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all_categories()

    @staticmethod
    def get_category_by_id(category_id):
        return CategoryRepository.get_category_by_id(category_id)

    @staticmethod
    def get_categories_by_company(company_id):
        return CategoryRepository.get_categories_by_company(company_id)

    @staticmethod
    def create_category(data):
        return CategoryRepository.create_category(data)

    @staticmethod
    def update_category(category_id, data):
        return CategoryRepository.update_category(category_id, data)

    @staticmethod
    def delete_category(category_id):
        return CategoryRepository.delete_category(category_id)
