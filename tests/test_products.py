from jsonschema import validate
import requests
from schemas import PRODUCT_SCHEMA

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
    validate(instance=products_list, schema=PRODUCT_SCHEMA)

# API phase 3 Homework:
# Step 3: 3. Getting one product by id returns 200 and the same data as that product in the list.
# Take the id from the list instead of writing 1.
# def test_get_one_product_return_200():
#     response_products = requests.get(f"/api/products")
#     product1_id = response_products.json()[0]["id"]
#     response = requests.get(f"/api/products/{product1_id}")

#     assert response.status_code == 200

# # API phase 3 Homework:
# # Step 3: 4. A product id that doesn't exist returns 404, and the body has an error message.
# def test_product_id_not_exist_return_404_error_message():
#     one_product_id = 9
#     response_products = requests.get(f"/api/products")
#     products_id = response_products.json()["id"]
#     if one_product_id not in products_id:
#         return products_id.status_code == 404 and "error: 404 product id doesn't exist"

# # API phase 3 Homework:
# # Step 3: 5. GET /api/products/abc. Predict the status first, then check it. 
# # Look at the content-type of the response too.
# def test_get_product_abc():
#     abc_response = requests.get(f"/api/products/abc")
#     return abc_response.status_code and abc_response.headers["content-type"]

