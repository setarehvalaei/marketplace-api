
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Marketplace API",
    description="Multi-Vendor Marketplace Backend",
    version="1.0.0"
)


products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 50000,
        "vendor_id": 1,
        "sold_count": 20,
        "stock": 10
    },
    {
        "id": 2,
        "name": "Headphones",
        "price": 2000,
        "vendor_id": 2,
        "sold_count": 50,
        "stock": 15
    }
]

vendors = [
    {"id": 1, "name": "Tech Store", "customer_count": 100},
    {"id": 2, "name": "Digital Shop", "customer_count": 200}
]

carts = {}
orders = []


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)


class CheckoutRequest(BaseModel):
    shipping_address: str = Field(min_length=5)



def find_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def find_vendor(vendor_id: int):
    for vendor in vendors:
        if vendor["id"] == vendor_id:
            return vendor
    return None


@app.get("/products")
def get_products():
    return products


@app.get("/products/best-selling")
def get_best_selling_products():
    return sorted(
        products,
        key=lambda product: product["sold_count"],
        reverse=True
    )


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = find_product(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@app.get("/vendors")
def get_vendors():
    return vendors


@app.get("/vendors/popular")
def get_popular_vendors():
    return sorted(
        vendors,
        key=lambda vendor: vendor["customer_count"],
        reverse=True
    )


@app.get("/vendors/{vendor_id}/products")
def get_vendor_products(vendor_id: int):
    vendor = find_vendor(vendor_id)

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    return [
        product for product in products
        if product["vendor_id"] == vendor_id
    ]


@app.get("/cart")
def get_cart():
    cart = carts.get(1, [])

    total = 0

    for item in cart:
        product = find_product(item["product_id"])
        if product:
            total += product["price"] * item["quantity"]

    return {
        "items": cart,
        "total": total
    }


@app.post("/cart/items", status_code=201)
def add_to_cart(data: CartItemCreate):
    product = find_product(data.product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if data.quantity > product["stock"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock"
        )

    cart = carts.setdefault(1, [])

    for item in cart:
        if item["product_id"] == data.product_id:
            new_quantity = item["quantity"] + data.quantity

            if new_quantity > product["stock"]:
                raise HTTPException(
                    status_code=400,
                    detail="Not enough stock"
                )

            item["quantity"] = new_quantity
            return item

    new_item = {
        "id": len(cart) + 1,
        "product_id": data.product_id,
        "quantity": data.quantity
    }

    cart.append(new_item)

    return new_item


@app.patch("/cart/items/{item_id}")
def update_cart_item(item_id: int, data: CartItemUpdate):
    cart = carts.get(1, [])

    for item in cart:
        if item["id"] == item_id:
            product = find_product(item["product_id"])

            if data.quantity > product["stock"]:
                raise HTTPException(
                    status_code=400,
                    detail="Not enough stock"
                )

            item["quantity"] = data.quantity
            return item

    raise HTTPException(
        status_code=404,
        detail="Cart item not found"
    )


@app.delete("/cart/items/{item_id}")
def remove_cart_item(item_id: int):
    cart = carts.get(1, [])

    for item in cart:
        if item["id"] == item_id:
            cart.remove(item)
            return {"message": "Item removed successfully"}

    raise HTTPException(
        status_code=404,
        detail="Cart item not found"
    )


@app.post("/orders", status_code=201)
def create_order(data: CheckoutRequest):
    cart = carts.get(1, [])

    if not cart:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    order_items = []
    total = 0

    for item in cart:
        product = find_product(item["product_id"])

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if item["quantity"] > product["stock"]:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product['name']}"
            )

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
        "shipping_address": data.shipping_address,
        "total": total,
        "status": "pending"
    }

    orders.append(order)

    carts[1] = []

    return order


@app.get("/orders")
def get_orders():
    return orders


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )
