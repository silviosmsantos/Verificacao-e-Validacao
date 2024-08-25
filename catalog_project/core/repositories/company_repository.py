from jsonschema import ValidationError
from core.models.company_models import Company

class CompanyRepository:
    @staticmethod
    def get_all_companies():
        return Company.objects.all()

    @staticmethod
    def get_company_by_id(company_id):
        return Company.objects.filter(id=company_id).first()

    @staticmethod
    def create_company(data):
        if Company.objects.filter(email=data['email']).exists():
            raise ValidationError("Já existe uma empresa cadastrada com este e-mail.")
        return Company.objects.create(**data)

    @staticmethod
    def update_company(company_id, data):
        company = Company.objects.filter(id=company_id).first()
        if company:
            for key, value in data.items():
                setattr(company, key, value)
            company.save()
        return company

    @staticmethod
    def delete_company(company_id):
        company = Company.objects.filter(id=company_id).first()
        if company:
            company.delete()
        return company
