from app.repositories.memory import products


def find_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return product

    return None