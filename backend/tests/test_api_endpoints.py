from datetime import date, timedelta

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.database import AsyncSessionLocal, Base, engine
from app.main import app
from app.models.domain import Property, RoomType


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Seed minimal data
    async with AsyncSessionLocal() as session:
        prop = Property(
            name="Test Boutique Hotel",
            slug="test-boutique-hotel",
            description="Test property for integration tests",
            city="Miami",
            address="123 Ocean Blvd",
            star_rating=4.5,
            review_score=9.0,
            review_count=50,
            image_url="https://images.unsplash.com/photo-1566073771259-6a8506099945",
            amenities="WiFi,Pool",
        )
        session.add(prop)
        await session.flush()

        room = RoomType(
            property_id=prop.id,
            name="Deluxe Suite",
            code="DELUXE_TEST",
            description="Test Room",
            base_price=200.0,
            total_rooms=2,
            max_occupancy=2,
            image_url="https://images.unsplash.com/photo-1582719478250-c89cae4dc85b",
        )
        session.add(room)
        await session.commit()


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_list_properties():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/properties")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Boutique Hotel"


@pytest.mark.asyncio
async def test_search_rooms():
    transport = ASGITransport(app=app)
    today = date.today()
    check_in = (today + timedelta(days=5)).isoformat()
    check_out = (today + timedelta(days=8)).isoformat()

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            f"/api/v1/search?city=Miami&check_in_date={check_in}&check_out_date={check_out}"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["room_name"] == "Deluxe Suite"
        assert len(data[0]["nightly_breakdown"]) == 3


@pytest.mark.asyncio
async def test_price_trend():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Fetch properties to get room_id
        props = await client.get("/api/v1/properties")
        prop_id = props.json()[0]["id"]
        rooms = await client.get(f"/api/v1/properties/{prop_id}/rooms")
        room_id = rooms.json()[0]["id"]

        trend_res = await client.get(f"/api/v1/pricing/trend?room_type_id={room_id}&days=14")
        assert trend_res.status_code == 200
        trend_data = trend_res.json()
        assert len(trend_data["points"]) == 14
        assert trend_data["room_name"] == "Deluxe Suite"


@pytest.mark.asyncio
async def test_create_and_fetch_booking():
    transport = ASGITransport(app=app)
    today = date.today()
    check_in = (today + timedelta(days=10)).isoformat()
    check_out = (today + timedelta(days=12)).isoformat()

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        props = await client.get("/api/v1/properties")
        prop_id = props.json()[0]["id"]
        rooms = await client.get(f"/api/v1/properties/{prop_id}/rooms")
        room_id = rooms.json()[0]["id"]

        payload = {
            "room_type_id": room_id,
            "guest_name": "Jane Doe",
            "guest_email": "jane@example.com",
            "check_in_date": check_in,
            "check_out_date": check_out,
            "guest_count": 2,
        }

        res = await client.post("/api/v1/bookings", json=payload)
        assert res.status_code == 201
        booking = res.json()
        assert booking["guest_name"] == "Jane Doe"
        assert "ZEN-" in booking["reservation_code"]

        # Fetch booking details by code
        code = booking["reservation_code"]
        get_res = await client.get(f"/api/v1/bookings/{code}")
        assert get_res.status_code == 200
        assert get_res.json()["guest_email"] == "jane@example.com"
