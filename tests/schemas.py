PRODUCT_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "price", "in_stock"], 
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "price": {"type": "number"}, 
        "in_stock": {"type": "boolean"}
    }
}