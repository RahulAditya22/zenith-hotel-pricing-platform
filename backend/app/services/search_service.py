from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.cache import get_cache
from app.models.domain import DemandEvent, Property, RoomType
from app.schemas.schemas import PriceTrendPoint, PriceTrendResponse, RoomSearchResult
from app.services.booking_service import BookingService
from app.services.pricing_engine import pricing_engine


class SearchService:
    @staticmethod
    async def search_rooms(
        session: AsyncSession,
        check_in_date: date,
        check_out_date: date,
        city: Optional[str] = None,
        guests: int = 1,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: str = "recommended",
    ) -> List[RoomSearchResult]:
        cache = get_cache()
        cache_key = f"search:{city}:{check_in_date}:{check_out_date}:{guests}:{min_price}:{max_price}:{sort_by}"
        cached_res = await cache.get(cache_key)
        if cached_res:
            return [RoomSearchResult(**item) for item in cached_res]

        # Fetch properties matching city
        prop_stmt = select(Property).options(selectinload(Property.room_types))
        if city:
            prop_stmt = prop_stmt.where(Property.city.ilike(f"%{city.strip()}%"))

        prop_res = await session.execute(prop_stmt)
        properties = prop_res.scalars().all()

        results: List[RoomSearchResult] = []
        night_count = (check_out_date - check_in_date).days

        for prop in properties:
            for room in prop.room_types:
                if room.max_occupancy < guests:
                    continue

                # Check booked rooms & availability
                booked_counts = await BookingService.get_booked_count_per_date(
                    session, room.id, check_in_date, check_out_date
                )
                max_booked = max(booked_counts.values()) if booked_counts else 0
                available_rooms = room.total_rooms - max_booked

                if available_rooms <= 0:
                    continue  # Exclude fully booked rooms

                # Calculate stay pricing
                total_price, breakdowns = await BookingService.calculate_stay_pricing(
                    session, room, check_in_date, check_out_date
                )
                avg_nightly = round(total_price / max(night_count, 1), 2)

                # Filter by price bounds if specified
                if min_price is not None and avg_nightly < min_price:
                    continue
                if max_price is not None and avg_nightly > max_price:
                    continue

                # Value score = (rating * score) / sqrt(avg_price) * 10
                value_score = round(
                    ((prop.review_score * prop.star_rating) / max(avg_nightly**0.5, 1.0)) * 10, 2
                )

                amenities_list = [a.strip() for a in prop.amenities.split(",") if a.strip()]

                item = RoomSearchResult(
                    property_id=prop.id,
                    property_name=prop.name,
                    property_city=prop.city,
                    star_rating=prop.star_rating,
                    review_score=prop.review_score,
                    review_count=prop.review_count,
                    property_image_url=prop.image_url,
                    property_amenities=amenities_list,
                    room_type_id=room.id,
                    room_name=room.name,
                    room_code=room.code,
                    room_image_url=room.image_url,
                    max_occupancy=room.max_occupancy,
                    total_rooms=room.total_rooms,
                    available_rooms=available_rooms,
                    total_price=total_price,
                    average_nightly_price=avg_nightly,
                    base_nightly_price=room.base_price,
                    value_score=value_score,
                    nightly_breakdown=breakdowns,
                )
                results.append(item)

        # Sorting logic
        if sort_by == "price_low":
            results.sort(key=lambda x: x.average_nightly_price)
        elif sort_by == "price_high":
            results.sort(key=lambda x: x.average_nightly_price, reverse=True)
        elif sort_by == "rating":
            results.sort(key=lambda x: x.review_score, reverse=True)
        else:  # "recommended"
            results.sort(key=lambda x: x.value_score, reverse=True)

        # Cache results for 300 seconds
        serializable_results = [item.model_dump(mode="json") for item in results]
        await cache.set(cache_key, serializable_results, ttl=300)

        return results

    @staticmethod
    async def get_price_trend(
        session: AsyncSession, room_type_id: int, days: int = 30, start_date: Optional[date] = None
    ) -> PriceTrendResponse:
        if start_date is None:
            start_date = date.today()
        end_date = start_date + timedelta(days=days)

        room_stmt = (
            select(RoomType)
            .options(selectinload(RoomType.property))
            .where(RoomType.id == room_type_id)
        )
        room_res = await session.execute(room_stmt)
        room = room_res.scalar_one_or_none()

        if not room:
            raise Exception(f"RoomType ID {room_type_id} not found")

        # Booked counts & events
        booked_counts = await BookingService.get_booked_count_per_date(
            session, room_type_id, start_date, end_date
        )

        event_stmt = select(DemandEvent).where(
            and_(
                DemandEvent.start_date <= end_date,
                DemandEvent.end_date >= start_date,
                (DemandEvent.property_id == room.property_id)
                | (DemandEvent.city == room.property.city),
            )
        )
        event_res = await session.execute(event_stmt)
        events = event_res.scalars().all()

        points: List[PriceTrendPoint] = []
        curr = start_date
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        while curr < end_date:
            booked = booked_counts.get(curr, 0)
            date_event = next((e for e in events if e.start_date <= curr <= e.end_date), None)
            e_mult = date_event.multiplier if date_event else 1.0
            e_name = date_event.name if date_event else None

            breakdown = pricing_engine.calculate_nightly_price(
                base_price=room.base_price,
                target_date=curr,
                booked_rooms=booked,
                total_rooms=room.total_rooms,
                booking_date=date.today(),
                event_multiplier=e_mult,
                event_name=e_name,
            )

            points.append(
                PriceTrendPoint(
                    date=curr,
                    day_name=day_names[curr.weekday()],
                    is_weekend=breakdown.is_weekend,
                    price=breakdown.final_price,
                    base_price=room.base_price,
                    occupancy_rate=breakdown.occupancy_rate,
                    occupancy_multiplier=breakdown.occupancy_multiplier,
                    lead_time_multiplier=breakdown.lead_time_multiplier,
                    event_multiplier=breakdown.demand_event_multiplier,
                    event_name=breakdown.demand_event_name,
                )
            )
            curr += timedelta(days=1)

        return PriceTrendResponse(
            property_id=room.property.id,
            property_name=room.property.name,
            room_type_id=room.id,
            room_name=room.name,
            base_price=room.base_price,
            start_date=start_date,
            end_date=end_date - timedelta(days=1),
            points=points,
        )
