import pytest, os
from playwright.sync_api import APIRequestContext, Playwright

PRODUCTS_BASE_URL = os.getenv("PRODUCTS_BASE_URL", "http://api:5000")

@pytest.fixture(scope="session")
def products_api(playwright: Playwright) -> APIRequestContext:
    #context = playwright.request.new_context(base_url=PRODUCTS_BASE_URL, timeout=10_000)
    context = playwright.request.new_context(base_url=PRODUCTS_BASE_URL, extra_http_headers={"X-Test-Run": "leon"}, timeout=10_000)
    yield context
    context.dispose()

from products_api import create_product, delete_product

@pytest.fixture
def new_product(products_api):
    payload = {"name": "Test Product", "price": 12.50, "in_stock": True}
    response = create_product(products_api, payload)
    assert response.status == 201, response.text()

    product = response.json()
    yield payload, product
    delete_product(products_api, product["id"])

@pytest.fixture
def get_payload(new_product):
    payload, _ = new_product
    return payload