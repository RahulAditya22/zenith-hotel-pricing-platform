import asyncio
import uuid
from datetime import date, timedelta
from typing import List, Optional, Tuple

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.cache import get_cache
from app.models.domain import DemandEvent, Reservation, RoomType
from app.schemas.schemas import PricingBreakdown, ReservationCreate
from app.services.pricing_engine import pricing_engine

# Process-level lock for concurrency safety across async tasks
_booking_lock = asyncio.Lock()


class BookingService:
    @staticmethod
    async def get_booked_count_per_date(
        session: AsyncSession, room_type_id: int, start_date: date, end_date: date
    ) -> dict[date, int]:
        """
        Calculates the number of confirmed booked rooms for each date in the range [start_date, end_date).
        """
        stmt = select(Reservation).where(
            and_(
                Reservation.room_type_id == room_type_id,
                Reservation.status == "CONFIRMED",
                Reservation.check_in_date < end_date,
                Reservation.check_out_date > start_date,
            )
        )
        result = await session.execute(stmt)
        reservations = result.scalars().all()

        date_counts: dict[date, int] = {}
        curr = start_date
        while curr < end_date:
            date_counts[curr] = 0
            curr += timedelta(days=1)

        for res in reservations:
            curr = max(res.check_in_date, start_date)
            res_end = min(res.check_out_date, end_date)
            while curr < res_end:
                if curr in date_counts:
                    date_counts[curr] += 1
                curr += timedelta(days=1)

        return date_counts

    @staticmethod
    async def calculate_stay_pricing(
        session: AsyncSession,
        room_type: RoomType,
        check_in_date: date,
        check_out_date: date,
        booking_date: Optional[date] = None,
    ) -> Tuple[float, List[PricingBreakdown]]:
        if check_out_date <= check_in_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="check_out_date must be after check_in_date",
            )

        if booking_date is None:
            booking_date = date.today()

        booked_counts = await BookingService.get_booked_count_per_date(
            session, room_type.id, check_in_date, check_out_date
        )

        city = room_type.property.city if room_type.property else None
        event_stmt = select(DemandEvent).where(
            and_(
                DemandEvent.start_date <= check_out_date,
                DemandEvent.end_date >= check_in_date,
                (DemandEvent.property_id == room_type.property_id) | (DemandEvent.city == city),
            )
        )
        event_res = await session.execute(event_stmt)
        events = event_res.scalars().all()

        nightly_breakdowns: List[PricingBreakdown] = []
        total_price = 0.0

        curr_date = check_in_date
        while curr_date < check_out_date:
            booked = booked_counts.get(curr_date, 0)

            date_event = next((e for e in events if e.start_date <= curr_date <= e.end_date), None)
            event_mult = date_event.multiplier if date_event else 1.0
            event_name = date_event.name if date_event else None

            breakdown = pricing_engine.calculate_nightly_price(
                base_price=room_type.base_price,
                target_date=curr_date,
                booked_rooms=booked,
                total_rooms=room_type.total_rooms,
                booking_date=booking_date,
                event_multiplier=event_mult,
                event_name=event_name,
            )

            nightly_breakdowns.append(breakdown)
            total_price += breakdown.final_price
            curr_date += timedelta(days=1)

        return round(total_price, 2), nightly_breakdowns

    @staticmethod
    async def create_reservation(session: AsyncSession, payload: ReservationCreate) -> Reservation:
        if payload.check_out_date <= payload.check_in_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="check_out_date must be after check_in_date",
            )

        async with _booking_lock:
            # Fetch room type with eagerly loaded property
            room_stmt = (
                select(RoomType)
                .options(selectinload(RoomType.property))
                .where(RoomType.id == payload.room_type_id)
            )
            room_res = await session.execute(room_stmt)
            room_type = room_res.scalar_one_or_none()

            if not room_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"RoomType ID {payload.room_type_id} not found",
                )

            if payload.guest_count > room_type.max_occupancy:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Guest count ({payload.guest_count}) exceeds max occupancy ({room_type.max_occupancy})",
                )

            booked_counts = await BookingService.get_booked_count_per_date(
                session, payload.room_type_id, payload.check_in_date, payload.check_out_date
            )

            max_booked = max(booked_counts.values()) if booked_counts else 0
            available_rooms = room_type.total_rooms - max_booked

            if available_rooms <= 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Room type '{room_type.name}' is fully booked for selected dates.",
                )

            total_price, _ = await BookingService.calculate_stay_pricing(
                session, room_type, payload.check_in_date, payload.check_out_date
            )

            night_count = (payload.check_out_date - payload.check_in_date).days
            reservation_code = f"ZEN-{uuid.uuid4().hex[:8].upper()}"

            reservation = Reservation(
                reservation_code=reservation_code,
                room_type_id=payload.room_type_id,
                guest_name=payload.guest_name,
                guest_email=payload.guest_email,
                check_in_date=payload.check_in_date,
                check_out_date=payload.check_out_date,
                guest_count=payload.guest_count,
                total_price=total_price,
                night_count=night_count,
                status="CONFIRMED",
            )

            session.add(reservation)
            await session.commit()

            # Invalidate cache
            cache = get_cache()
            await cache.clear()

            return reservation
