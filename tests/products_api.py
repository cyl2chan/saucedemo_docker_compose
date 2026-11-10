from playwright.sync_api import APIRequestContext, APIResponse

PRODUCTS = "/api/products"

def get_products(api: APIRequestContext) -> APIResponse:
    return api.get(PRODUCTS)

def get_product(api: APIRequestContext, product_id) -> APIResponse:
    return api.get(f"{PRODUCTS}/{product_id}")

def create_product(api: APIRequestContext, payload) -> APIResponse:
    return api.post(PRODUCTS, data=payload)

# Step 2: Write the other three yourself: 
# delete_product(api, product_id), replace_product(api, product_id, payload), update_product(api, product_id, payload).
# Use the Playwright docs to find the method for each.

def delete_product(api: APIRequestContext, product_id) -> APIResponse:
    return api.delete(f"{PRODUCTS}/{product_id}")

def replace_product(api: APIRequestContext, product_id, payload) -> APIResponse:
    return api.put(f"{PRODUCTS}/{product_id}", data=payload)

def update_product(api: APIRequestContext, product_id, payload) -> APIResponse:
    return api.patch(f"{PRODUCTS}/{product_id}", data=payload)