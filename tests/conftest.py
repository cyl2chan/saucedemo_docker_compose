import pytest, os
from playwright.sync_api import APIRequestContext, APIResponse, Playwright

PRODUCTS_BASE_URL = os.getenv("PRODUCTS_BASE_URL", "http://localhost:5000")

@pytest.fixture(scope="session")
def products_api(playwright: Playwright) -> APIRequestContext:
    context = playwright.request.new_context(base_url=PRODUCTS_BASE_URL, timeout=10_000)
    yield context
    context.dispose()


