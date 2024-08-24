import pytest
from django.conf import settings

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    # This fixture is intentionally left empty. It automatically grants database 
    # access to all tests by including the 'db' fixture. Since no additional setup 
    # is needed, no implementation is required here.
    pass
