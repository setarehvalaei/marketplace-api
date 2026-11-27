from fastapi import APIRouter, HTTPException

from app.repositories.memory import vendors, products
from app.services.vendor_service import find_vendor


router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("/")
def get_vendors():
    return vendors


@router.get("/popular")
def get_popular_vendors():
    return sorted(
        vendors,
        key=lambda vendor: vendor["customer_count"],
        reverse=True
    )


@router.get("/{vendor_id}/products")
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