from fastapi import APIRouter, HTTPException

from app.repositories.memory import orders
from app.schemas.order import CheckoutRequest
from app.services.order_service import create_order
from app.services.product_service import find_product


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", status_code=201)
def checkout(request: CheckoutRequest):
    try:
        return create_order(
            shipping_address=request.shipping_address,
            find_product=find_product
        )

    except ValueError as error:
        if str(error) == "Cart is empty":
            raise HTTPException(status_code=400, detail=str(error))

        if str(error) == "Product not found":
            raise HTTPException(status_code=404, detail=str(error))

        if str(error) == "Not enough stock":
            raise HTTPException(status_code=400, detail=str(error))

        raise


@router.get("/")
def get_orders():
    return orders


@router.get("/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )