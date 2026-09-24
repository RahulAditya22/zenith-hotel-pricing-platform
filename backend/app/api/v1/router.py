from fastapi import APIRouter

from app.api.v1.endpoints import bookings, pricing, properties, search

api_router = APIRouter()

api_router.include_router(properties.router, prefix="/properties", tags=["Properties & Rooms"])
api_router.include_router(search.router, prefix="/search", tags=["Search & Availability"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["Reservations & Booking"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["Dynamic Pricing Engine"])
