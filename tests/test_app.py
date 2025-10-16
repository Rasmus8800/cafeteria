import http

import httpx
import pytest

pytestmark = [pytest.mark.asyncio]


async def test_app_docs(test_client: httpx.AsyncClient) -> None:
    """Проверяет, что документация API доступна."""
    async with test_client:
        response = await test_client.get("/docs")

    assert response.status_code == http.HTTPStatus.OK
    assert "text/html" in response.headers["content-type"]


async def test_app_openapi_schema(test_client: httpx.AsyncClient):
    """Проверяет OpenAPI схему асинхронно."""
    async with test_client:
        response = await test_client.get("/openapi.json")

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema
