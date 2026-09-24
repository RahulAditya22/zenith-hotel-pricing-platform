"""Reservation creation and lookup endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.domain import Reservation
from app.schemas.schemas import (
    ReservationCreate,
    ReservationResponse,
)
from app.services.booking_service import BookingService

router = APIRouter()


@router.post(
    "",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking(
    payload: ReservationCreate,
    db: AsyncSession = Depends(get_db),
):
    reservation = await BookingService.create_reservation(
        db, payload,
    )
    return reservation


@router.get(
    "/{reservation_code}",
    response_model=ReservationResponse,
)
async def get_booking_details(
    reservation_code: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Reservation).where(
        Reservation.reservation_code == reservation_code,
    )
    res = await db.execute(stmt)
    booking = res.scalar_one_or_none()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Reservation code {reservation_code}"
                " not found"
            ),
        )
    return booking
