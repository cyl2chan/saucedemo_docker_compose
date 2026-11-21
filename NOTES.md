
| Input | Expected status | Why | Actual
|---|---|---|
| Wrong type: number of price in quotes "6.00" | 400 Bad Request or 422 Unprocessable Content | Wrong type is a problem, which cause server to reject it / Unable to process the value | 201 Created
| in_stock == Yes | 400 Bad Request or 422 Unprocessable Content | Wrong type is a problem, which cause server to reject it / Unable to process the value | 201 Created
| number as name | 400 Bad Request or 422 Unprocessable Content | Wrong type is a problem, which cause server to reject it / Unable to process the value | 201 Created

| Empty and missing: empty name | 400 Bad Request | Name is required for a product to be created |
| null for name | 400 Bad Request | Name is required for a product to be created |
| empty body {} | 400 Bad Request | Information of name, price, and in_stock are required for a product to be created |

| Too long a name: 100 | 201 | Since number of characters is within limit, product will be successfully created |
| Too long a name: 101 | 400 Bad Request or 422 Unprocessable Content | Since input of name has exceeded limit, it's a problem or unable to process the value |

| Price make no sense: negative, very large, zero, empty, null, letter, sympbols |400 Bad Request or 422 Unprocessable Content| Since it makes on sense, it's a problem or unable to process the value |

| Extra field API doesn't know about eg. country made from | 404 Not Found | Extra field doesn't exist in API |
| Duplicate entry: product with same name in one of items in database | 409 COnflict | Same item has already exist |