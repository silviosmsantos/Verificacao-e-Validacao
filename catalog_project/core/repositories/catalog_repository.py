from core.models.catalog_models import Catalog

class CatalogRepository:
    @staticmethod
    def create_catalog(data):
        return Catalog.objects.create(**data)

    @staticmethod
    def get_catalog_by_id(catalog_id):
        try:
            return Catalog.objects.get(id=catalog_id)
        except Catalog.DoesNotExist:
            return None

    @staticmethod
    def get_all_catalogs():
        return Catalog.objects.all()

    @staticmethod
    def update_catalog(catalog_id, data):
        catalog = CatalogRepository.get_catalog_by_id(catalog_id)
        if catalog:
            for key, value in data.items():
                setattr(catalog, key, value)
            catalog.save()
        return catalog

    @staticmethod
    def delete_catalog(catalog_id):
        catalog = CatalogRepository.get_catalog_by_id(catalog_id)
        if catalog:
            catalog.delete()
        return catalog
