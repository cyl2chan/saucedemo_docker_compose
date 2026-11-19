# API phase 3 Homework:
# Step 3: 2. Every product in the list matches a PRODUCT_SCHEMA you add to schemas.py. 
# Reuse what you learned in Phase 2: which fields are required, and what type is each one?

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