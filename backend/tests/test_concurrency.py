import asyncio
from datetime import date, timedelta

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.database import AsyncSessionLocal, Base, engine
from app.main import app
from app.models.domain import Property, RoomType


@pytest.fixture(autouse=True)
async def setup_single_room_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        prop = Property(
            name="Single Room Haven",
            slug="single-room-haven",
            description="Boutique hotel with only 1 exclusive penthouse suite",
            city="Aspen",
            address="1 Peak Way",
            star_rating=5.0,
            review_score=9.8,
            review_count=20,
            image_url="https://images.unsplash.com/photo-1566073771259-6a8506099945",
            amenities="WiFi,Spa",
        )
        session.add(prop)
        await session.flush()

        room = RoomType(
            property_id=prop.id,
            name="Exclusive Penthouse",
            code="PENTHOUSE_EXCLUSIVE",
            description="Single room type with total_rooms=1",
            base_price=500.0,
            total_rooms=1,  # EXACTLY 1 ROOM TOTAL
            max_occupancy=2,
            image_url="https://images.unsplash.com/photo-1582719478250-c89cae4dc85b",
        )
        session.add(room)
        await session.commit()


@pytest.mark.asyncio
async def test_concurrent_booking_prevents_double_booking():
    transport = ASGITransport(app=app)
    today = date.today()
    check_in = (today + timedelta(days=5)).isoformat()
    check_out = (today + timedelta(days=8)).isoformat()

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        props = await client.get("/api/v1/properties")
        prop_id = props.json()[0]["id"]
        rooms = await client.get(f"/api/v1/properties/{prop_id}/rooms")
        room_id = rooms.json()[0]["id"]

        payload_1 = {
            "room_type_id": room_id,
            "guest_name": "Alice Speed",
            "guest_email": "alice@example.com",
            "check_in_date": check_in,
            "check_out_date": check_out,
            "guest_count": 2,
        }

        payload_2 = {
            "room_type_id": room_id,
            "guest_name": "Bob Speed",
            "guest_email": "bob@example.com",
            "check_in_date": check_in,
            "check_out_date": check_out,
            "guest_count": 2,
        }

        # Launch both booking HTTP requests concurrently using asyncio.gather
        task1 = client.post("/api/v1/bookings", json=payload_1)
        task2 = client.post("/api/v1/bookings", json=payload_2)

        res1, res2 = await asyncio.gather(task1, task2, return_exceptions=True)

        statuses = [res1.status_code, res2.status_code]
        print(f"Concurrent booking responses: {statuses}")

        # One must be 201 CREATED, and the other must be 409 CONFLICT
        assert 201 in statuses, "One booking must succeed"
        assert 409 in statuses, "One booking must fail with 409 Conflict due to capacity lock"
