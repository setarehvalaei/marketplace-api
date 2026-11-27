from app.repositories.memory import carts


def get_user_cart(user_id=1):
    return carts.setdefault(user_id, [])


def calculate_cart_total(cart, find_product):
    total = 0

    for item in cart:
        product = find_product(item["product_id"])

        if product:
            total += product["price"] * item["quantity"]

    return total