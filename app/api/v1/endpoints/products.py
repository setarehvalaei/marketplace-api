from fastapi import APIRouter, HTTPException

from app.repositories.memory import products
from app.services.product_service import find_product


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def get_products():
    return products


@router.get("/best-selling")
def get_best_selling_products():
    return sorted(
        products,
        key=lambda product: product["sold_count"],
        reverse=True
    )


@router.get("/{product_id}")
def get_product(product_id: int):
    product = find_product(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product