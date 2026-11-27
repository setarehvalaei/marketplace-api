from fastapi import APIRouter, HTTPException

from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.services.cart_service import get_user_cart, calculate_cart_total
from app.services.product_service import find_product


router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/")
def get_cart():
    cart = get_user_cart()
    total = calculate_cart_total(cart, find_product)

    return {
        "items": cart,
        "total": total
    }


@router.post("/items", status_code=201)
def add_cart_item(item: CartItemCreate):
    product = find_product(item.product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if item.quantity > product["stock"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock"
        )

    cart = get_user_cart()

    for cart_item in cart:
        if cart_item["product_id"] == item.product_id:
            new_quantity = cart_item["quantity"] + item.quantity

            if new_quantity > product["stock"]:
                raise HTTPException(
                    status_code=400,
                    detail="Not enough stock"
                )

            cart_item["quantity"] = new_quantity
            return cart_item

    new_item = {
        "id": len(cart) + 1,
        "product_id": item.product_id,
        "quantity": item.quantity
    }

    cart.append(new_item)
    return new_item


@router.patch("/items/{item_id}")
def update_cart_item(item_id: int, item: CartItemUpdate):
    cart = get_user_cart()

    for cart_item in cart:
        if cart_item["id"] == item_id:
            product = find_product(cart_item["product_id"])

            if item.quantity > product["stock"]:
                raise HTTPException(
                    status_code=400,
                    detail="Not enough stock"
                )

            cart_item["quantity"] = item.quantity
            return cart_item

    raise HTTPException(
        status_code=404,
        detail="Cart item not found"
    )


@router.delete("/items/{item_id}")
def remove_cart_item(item_id: int):
    cart = get_user_cart()

    for cart_item in cart:
        if cart_item["id"] == item_id:
            cart.remove(cart_item)
            return {"message": "Item removed from cart"}

    raise HTTPException(
        status_code=404,
        detail="Cart item not found"
    )