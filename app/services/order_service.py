from app.repositories.memory import orders
from app.services.cart_service import get_user_cart


def create_order(shipping_address, find_product, user_id=1):
    cart = get_user_cart(user_id)

    if not cart:
        raise ValueError("Cart is empty")

    order_items = []
    total = 0

    for item in cart:
        product = find_product(item["product_id"])

        if not product:
            raise ValueError("Product not found")

        if item["quantity"] > product["stock"]:
            raise ValueError("Not enough stock")

        subtotal = product["price"] * item["quantity"]
        total += subtotal

        order_items.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "vendor_id": product["vendor_id"],
            "quantity": item["quantity"],
            "unit_price": product["price"],
            "subtotal": subtotal
        })

    for item in cart:
        product = find_product(item["product_id"])
        product["stock"] -= item["quantity"]

    order = {
        "id": len(orders) + 1,
        "items": order_items,
        "shipping_address": shipping_address,
        "total": total,
        "status": "pending"
    }

    orders.append(order)
    cart.clear()

    return order