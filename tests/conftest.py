import httpx
import pytest
from cafeteria.app import app

CAFETERIA_BASE_URL = "https://cafetria.ru/"


@pytest.fixture
def test_client() -> httpx.AsyncClient:
    """Фикстура для тестового клиента FastAPI."""
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(base_url=CAFETERIA_BASE_URL, transport=transport)
