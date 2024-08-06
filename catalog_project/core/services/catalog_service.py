# core/services/catalog_service.py
from core.repositories.catalog_repository import CatalogRepository
from core.validators.catalog_validator import validate_catalog_data

class CatalogService:
    @staticmethod
    def create_catalog(data):
        validate_catalog_data(data)
        return CatalogRepository.create_catalog(data)

    @staticmethod
    def get_catalog(catalog_id):
        return CatalogRepository.get_catalog_by_id(catalog_id)

    @staticmethod
    def update_catalog(catalog_id, data):
        validate_catalog_data(data, is_update=True)
        return CatalogRepository.update_catalog(catalog_id, data)

    @staticmethod
    def delete_catalog(catalog_id):
        return CatalogRepository.delete_catalog(catalog_id)
