from fastapi import FastAPI

from app.api.v1.endpoints import (
    products,
    vendors,
    cart,
    orders
)


app = FastAPI(
    title="Marketplace API",
    description="Multi-Vendor Marketplace Backend",
    version="1.0.0"
)


app.include_router(products.router)
app.include_router(vendors.router)
app.include_router(cart.router)
app.include_router(orders.router)