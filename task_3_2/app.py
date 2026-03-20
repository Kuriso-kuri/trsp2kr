from fastapi import FastAPI, Query

app = FastAPI()

sample_products = [
    {
        "product_id": 123,
        "name": "Smartphone",
        "category": "Electronics",
        "price": 599.99
    },
    {
        "product_id": 456,
        "name": "Phone Case",
        "category": "Accessories",
        "price": 19.99
    },
    {
        "product_id": 789,
        "name": "Iphone",
        "category": "Electronics",
        "price": 1299.99
    },
    {
        "product_id": 101,
        "name": "Headphones",
        "category": "Accessories",
        "price": 99.99
    },
    {
        "product_id": 202,
        "name": "Smartwatch",
        "category": "Electronics",
        "price": 299.99
    }
]

@app.get("/product/{product_id}")
def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    return {"message": "Product not found"}

@app.get("/products/search")
def search_products(
    keyword: str,
    category: str = None,
    limit: int = 10
):
    results = []

    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            if category:
                if product["category"].lower() != category.lower():
                    continue
            results.append(product)

    return results[:limit]