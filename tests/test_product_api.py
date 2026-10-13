"""
API Tests — these run inside the 'test-runner' container and hit the 'api' container.
Notice how we use http://api:5000 — 'api' is the service name from docker-compose.yml.
Docker's internal DNS resolves it automatically. No localhost, no IP addresses.
"""
import pytest
import requests
import time
import os

# The API URL comes from docker-compose environment variable, with a fallback
BASE_URL = os.environ.get("API_URL", "http://api:5000")


# ─── Helper: Wait for API to be Ready ────────────────────

def wait_for_api(retries=15, delay=2):
    """Poll the health endpoint until the API + DB are both up."""
    for attempt in range(retries):
        try:
            r = requests.get(f"{BASE_URL}/health", timeout=3)
            if r.status_code == 200:
                print(f"API ready after {attempt + 1} attempt(s)")
                return
        except requests.ConnectionError:
            pass
        print(f"API not ready, retrying in {delay}s... ({attempt + 1}/{retries})")
        time.sleep(delay)
    raise Exception("API never became ready")


# Runs once before all tests in this file
@pytest.fixture(scope="session", autouse=True)
def api_ready():
    wait_for_api()


# ─── GET Tests ───────────────────────────────────────────

class TestGetProducts:
    """Tests for the GET /api/products endpoint."""

    def test_get_all_products_returns_200(self):
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200

    def test_get_all_products_returns_list(self):
        response = requests.get(f"{BASE_URL}/api/products")
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 4  # We seeded 4 products

    def test_product_has_required_fields(self):
        """Validate the response schema — every product must have these keys."""
        response = requests.get(f"{BASE_URL}/api/products")
        data = response.json()
        required_fields = {"id", "name", "price", "in_stock"}
        for product in data:
            assert required_fields.issubset(product.keys()), \
                f"Product missing fields: {required_fields - product.keys()}"

    def test_get_single_product(self):
        response = requests.get(f"{BASE_URL}/api/products/1")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Sauce Labs Backpack"
        assert data["price"] == 29.99

    def test_get_nonexistent_product_returns_404(self):
        response = requests.get(f"{BASE_URL}/api/products/9999")
        assert response.status_code == 404


# ─── Parametrized Price Validation ───────────────────────

@pytest.mark.parametrize("product_id, expected_name, expected_price", [
    (1, "Sauce Labs Backpack", 29.99),
    (2, "Sauce Labs Bike Light", 9.99),
    (3, "Sauce Labs Bolt T-Shirt", 15.99),
])
def test_product_prices_match_catalog(product_id, expected_name, expected_price):
    """Parametrized test — validates each product's price against the catalog."""
    response = requests.get(f"{BASE_URL}/api/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == expected_name
    assert data["price"] == expected_price


# ─── POST Tests ──────────────────────────────────────────

class TestCreateProduct:
    """Tests for POST /api/products."""

    def test_create_product_returns_201(self):
        payload = {"name": "Test Widget", "price": 5.99, "in_stock": True}
        response = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Widget"
        assert "id" in data  # DB assigned an ID

    def test_create_product_missing_name_returns_400(self):
        payload = {"price": 5.99}
        response = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert response.status_code == 400

    def test_create_product_missing_price_returns_400(self):
        payload = {"name": "No Price Item"}
        response = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert response.status_code == 400


# ─── Chained Test: Create → Read → Delete → Verify ──────

class TestProductLifecycle:
    """
    Full CRUD chain — this is a KEY interview topic.
    'How do you test API operations that depend on each other?'
    """

    def test_full_product_lifecycle(self):
        # 1) CREATE a new product
        payload = {"name": "Lifecycle Test Item", "price": 42.00, "in_stock": True}
        create_response = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert create_response.status_code == 201
        product_id = create_response.json()["id"]

        # 2) READ — verify it exists
        read_response = requests.get(f"{BASE_URL}/api/products/{product_id}")
        assert read_response.status_code == 200
        assert read_response.json()["name"] == "Lifecycle Test Item"

        # 3) DELETE it
        delete_response = requests.delete(f"{BASE_URL}/api/products/{product_id}")
        assert delete_response.status_code == 200

        # 4) VERIFY it's gone
        verify_response = requests.get(f"{BASE_URL}/api/products/{product_id}")
        assert verify_response.status_code == 404


# Homework 15.
# -- Chained Test 2: Create a new product -> fetches all products -> verifies the new product is present --
class TestCreateProductAndVerify:
    def test_create_product_verify(self): 
        # 1) CREATE a new product 
        payload = {"name": "Test Item 2", "price": 29.99, "in_stock": True}
        create_response = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert create_response.status_code == 201
        product_id = create_response.json()["id"]

        # 2) READ - fetches all products and VERIFY the new one is on the list
        read_all_response = requests.get(f"{BASE_URL}/api/products")
        assert read_all_response.status_code == 200

        # 3) VERIFY new product is on the list
        read_response = requests.get(f"{BASE_URL}/api/products/{product_id}")
        assert read_response.status_code == 200
        assert read_response.json()["name"] == "Test Item 2"


# ─── Health Check ────────────────────────────────────────

def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
