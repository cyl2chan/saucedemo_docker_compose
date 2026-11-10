import requests

def get_products_return_200_and_list(self):
    response = requests.get(f"/api/products")
    products_list = response.json()
    return response.status_code and products_list