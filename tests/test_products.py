from jsonschema import validate
from schemas import PRODUCT_SCHEMA
from products_api import create_product, delete_product
import pytest

# API phase 3 Homework:
# Step 3: 1. GET /api/products returns 200 and a list.
def test_get_products_return_200_and_list(products_api):
    response = products_api.get(f"/api/products")
    products_list = response.json()
    assert response.status == 200, response.text()
    assert isinstance(products_list, list)

# API phase 3 Homework:
# Step 3: 2. Every product in the list matches a PRODUCT_SCHEMA you add to schemas.py. 
# Reuse what you learned in Phase 2: which fields are required, and what type is each one?
def test_schema(products_api):
    response = products_api.get(f"/api/products")
    products_list = response.json()
    for product in products_list:
        validate(instance=product, schema=PRODUCT_SCHEMA)

# API phase 3 Homework:
# Step 3: 3. Getting one product by id returns 200 and the same data as that product in the list.
# Take the id from the list instead of writing 1
def test_get_one_product_return_200_and_same_data_in_list(products_api):
    response_products = products_api.get(f"/api/products")
    product1_id = response_products.json()[0]["id"]
    response = products_api.get(f"/api/products/{product1_id}")
    product1 = response.json()
    assert response.status == 200

    # Assert data (ie. id, name, price, in_stock) in the product is same as that in the list. 
    list_product1_id = response_products.json()[0]["id"]
    list_product1_name = response_products.json()[0]["name"]
    list_product1_price = response_products.json()[0]["price"]
    list_product1_in_stock = response_products.json()[0]["in_stock"]

    product1_id = response.json()["id"]
    product1_name = response.json()["name"]
    product1_price = response.json()["price"]
    product1_in_stock = response.json()["in_stock"]
    
    assert list_product1_id == product1_id, f"list_product1_id = {list_product1_id}; product1_id = {product1_id}"
    assert list_product1_name == product1_name, f"list_product1_name = {list_product1_name}; product1_name = {product1_name}"
    assert list_product1_price == product1_price, f"list_product1_price = {list_product1_price}; product1_id = {product1_price}"
    assert list_product1_in_stock == product1_in_stock, f"list_product1_in_stock = {list_product1_in_stock}; product1_in_stock = {product1_in_stock}"


# API phase 3 Homework:
# Step 3: 4. A product id that doesn't exist returns 404, and the body has an error message.
def test_product_id_not_exist_return_404_error_message(products_api):
    one_product_id = 9999999999
    response_product = products_api.get(f"/api/products/{one_product_id}")
    assert response_product.status == 404
    assert "error" in response_product.text(), f"response_product.text(): {response_product.text()}"
    print(f"response_product.text(): {response_product.text()}")
    

# API phase 3 Homework:
# Step 3: 5. GET /api/products/abc. Predict the status first, then check it. 
# Look at the content-type of the response too.
def test_get_product_abc(products_api):
    abc_response = products_api.get(f"/api/products/abc")
    assert abc_response.status == 404
    assert abc_response.headers["content-type"]
    print(f"abc_response.headers['content-type']: {abc_response.headers['content-type']}")

# API phase 3 Homework:
# Step 4: Create a product, and check the receipt
# The response to a POST is the server saying it created something. 
# A receipt is when you read it back to prove the change really happened. Start from this skeleton:
def test_create_product(products_api):
    payload = {"name": "Leon Test Mug", "price": 8.50, "in_stock": False}
    response = create_product(products_api, payload)
    assert response.status == 201, response.text()
    created = response.json()

    # TODO 1: every field in payload comes back unchanged in created, and created has an "id"
    assert created["name"] == "Leon Test Mug"
    assert created["price"] == 8.50
    assert created["in_stock"] == False
    assert "id" in created

    # TODO 2 (the receipt): GET the product by its id and check it matches created
    # TODO 3: the new id appears in GET /api/products
    response_products_list = products_api.get("/api/products")
    products = response_products_list.json()
    def product_id():
        for product in products:
            if product["name"] == "Leon Test Mug":
                return product["id"]
    print("products:", products)
    print("product_id():", product_id(), "; created['id']:", created['id'])
    assert product_id() == created["id"], f"product_id(): {product_id()}; created['id']: {created['id']}"

    # TODO 4: clean up by deleting the product
    response_delete = products_api.delete(f"/api/products/{product_id()}")
    assert response_delete.status == 200

# API phase 3 Homework:
# Step 5: A fixture that creates and cleans up
# Rewrite your Step 3 single-product test to use new_product in conftest.py
def test_rewrite_create_product(products_api, new_product):
    # TODO 1: every field in payload comes back unchanged in created, and created has an "id"
    assert new_product["name"] == "Test Product"
    assert new_product["price"] == 12.50
    assert new_product["in_stock"] == True
    assert "id" in new_product

    # TODO 2 (the receipt): GET the product by its id and check it matches created
    # TODO 3: the new id appears in GET /api/products
    response_products_list = products_api.get("/api/products")
    products = response_products_list.json()
    def product_id():
        for product in products:
            if product["name"] == "Test Product":
                return product["id"]
    print("products:", products)
    print("product_id():", product_id(), "; new_product['id']:", new_product['id'])
    assert product_id() == new_product["id"], f"product_id(): {product_id()}; new_product['id']: {new_product['id']}"

    # TODO 4: clean up by deleting the product
    # code to delete product is in conftest.py and products_api.py

# API phase 3 Homework:
# Step 6: Bad input on POST, and hunting for bugs
@pytest.mark.parametrize("payload", [
    {"price": 5.00},      # missing name
    {"name": "No Price"}, # missing price
])
def test_create_product_missing_field(products_api, payload):
    response = create_product(products_api, payload)
    assert response.status == 400
    assert response.json()["error"]

# design my own bad inputs

@pytest.mark.parametrize("wrong_type_payload", [
    {"name": "Test Earbuds One", "price": "9.99", "in_stock": True},
    {"name": "Test Earbuds Two", "price": 9.99, "in_stock": "Yes"},
    {"name": 999, "price": 9.99, "in_stock": True},
])
def test_create_product_wrong_type(products_api, wrong_type_payload):
    response = create_product(products_api, wrong_type_payload)

    try: 
        print("response.status:", response.status)
        assert response.status == 400
        assert response.json()["error"]
    except: 
        products_list = products_api.get("/api/products")
        products = products_list.json()

        payload_names = [wrong_type_payload["name"]]
        print("payload_names:", payload_names)

        def find_product_id(payload_names):
            payload_ids = [] 
            for product in products:
                if product["name"] in payload_names:
                    payload_ids.append(product["id"])
            return payload_ids

        for payload_id in find_product_id(payload_names):
            response_delete = delete_product(products_api, payload_id)
            assert response_delete.status == 200
    
# def test_create_product_wrong_type(products_api, wrong_type_payload):
#     response = create_product(products_api, wrong_type_payload)

#     if response.status == 201:
#         product_id = response.json()["id"]
#         cleanup = delete_product(products_api, product_id)
#         assert cleanup.status == 200, cleanup.text()

#     assert response.status == 400, response.text()
#     assert response.json().get("error"), response.text()


# | Empty and missing: empty name | 400 Bad Request | Name is required for a product to be created |
# | null for name | 400 Bad Request | Name is required for a product to be created |
# | empty body {} | 400 Bad Request | Information of name, price, and in_stock are required for a product to be created |
# @pytest.mark.parametrize("empty_missing_payload", [
#     {"name": "", "price": 9.99, "in_stock": True},
#     {"name": None, "price": 9.99, "in_stock": True},
#     {},
# ])
# def test_create_empty_missing_payload(products_api, empty_missing_payload):
#     response = create_product(products_api, empty_missing_payload)
#     new_products = response.json()



# # | Too long a name: try 100, 101 | 400 Bad Request or 422 Unprocessable Content | Since input of name has exceeded limit, it's a problem or unable to process the value |
# @pytest.mark.parametrize("too_long_name_payload", [
#     {"name": "Advanced Waterproof Outdoor Hiking Backpack with Adjustable Straps and Multiple Storage Compartments", "price": 9.99, "in_stock": True},
#     {"name": "Excellent Waterproof Outdoor Hiking Backpack with Adjustable Straps and Multiple Storage Compartments", "price": 9.99, "in_stock": True},
# ])

# # | Price make no sense: negative, very large, zero, empty, null, letter, sympbols |400 Bad Request or 422 Unprocessable Content| Since it makes on sense, it's a problem or unable to process the value |
# @pytest.mark.parametrize("price_no_sense_payload", [
#     {"name": "Test Headphone One", "price": -9.99, "in_stock": True},
#     {"name": "Test Headphone Two", "price": 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999, "in_stock": True},
#     {"name": "Test Headphone Three", "price": 0, "in_stock": True},
#     {"name": "Test Headphone Four", "price": "", "in_stock": True},
#     {"name": "Test Headphone Five", "price": None, "in_stock": True},
#     {"name": "Test Headphone Six", "price": "hello", "in_stock": True},
#     {"name": "Test Headphone Seven", "price": hello, "in_stock": True},
#     {"name": "Test Headphone Eight", "price": "$", "in_stock": True},
# ])

# #| Extra field API doesn't know about eg. country made from | 404 Not Found | Extra field doesn't exist in API |
# @pytest.mark.parametrize("Extra_field_payload", [
#     {"name": "Test Keyboard One", "price": 9.99, "in_stock": True, "made_from": "Canada"},
#     {"name": "Test Keyboard Two", "price": 9.99, "in_stock": True, "manufacture_date": "Nov 18, 2022"},
#     {"name": "Test Keyboard Three", "price": 9.99, "in_stock": True, "color": "red"},
# ])

# #| Duplicate entry: product with same name in one of items in database | 409 COnflict | Same item has already exist |
# @pytest.mark.parametrize("duplicate_payload", [
#     {"name": "Sauce Labs Backpack", "price": 29.99, "in_stock": True},
#     {"name": "Sauce Labs Backpack", "price": 9.99, "in_stock": True},
#     {"name": "Sauce Labs Bike Light", "price": 9.99, "in_stock": True},
#     {"name": "Sauce Labs Bike Light", "price": 7.99, "in_stock": True},
#     {"name": "Sauce Labs Bolt T-Shirt", "price": 15.99, "in_stock": True},
#     {"name": "Sauce Labs Bolt T-Shirt", "price": 49.99, "in_stock": True},
#     {"name": "Sauce Labs Fleece Jacket", "price": 49.99, "in_stock": False},
#     {"name": "Sauce Labs Fleece Jacket", "price": 39.99, "in_stock": False},
# ])


