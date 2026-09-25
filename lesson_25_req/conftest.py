import pytest
from api.client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api_client():
    return APIClient(BASE_URL)