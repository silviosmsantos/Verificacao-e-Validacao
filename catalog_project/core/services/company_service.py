from core.repositories.company_repository import CompanyRepository

class CompanyService:
    @staticmethod
    def get_all_companies():
        return CompanyRepository.get_all_companies()

    @staticmethod
    def get_company_by_id(company_id):
        return CompanyRepository.get_company_by_id(company_id)

    @staticmethod
    def create_company(data):
        return CompanyRepository.create_company(data)

    @staticmethod
    def update_company(company_id, data):
        return CompanyRepository.update_company(company_id, data)

    @staticmethod
    def delete_company(company_id):
        return CompanyRepository.delete_company(company_id)
