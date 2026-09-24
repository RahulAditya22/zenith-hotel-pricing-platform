import asyncio
import os
import sys
from datetime import date, timedelta

# Ensure parent directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import AsyncSessionLocal, Base, engine
from app.models.domain import DemandEvent, Property, Reservation, RoomType

PROPERTIES_DATA = [
    {
        "name": "Zenith Ocean Resort & Spa",
        "slug": "zenith-ocean-resort-miami",
        "description": "Exclusive oceanfront sanctuary in South Beach featuring private cabanas, infinity pools, and world-class dining.",
        "city": "Miami",
        "state": "FL",
        "country": "USA",
        "address": "1001 Ocean Drive, South Beach, FL 33139",
        "star_rating": 5.0,
        "review_score": 9.4,
        "review_count": 320,
        "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Oceanfront,Infinity Pool,Luxury Spa,Private Beach,Fine Dining,Valet Parking",
        "room_types": [
            {
                "name": "Ocean King Suite",
                "code": "MIAMI_OCEAN_KING",
                "description": "Floor-to-ceiling glass walls overlooking the Atlantic Ocean, private balcony, marble bath.",
                "base_price": 380.0,
                "total_rooms": 12,
                "max_occupancy": 2,
                "amenities": "Balcony,King Bed,Ocean View,Nespresso Machine,Soaking Tub",
                "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1000&q=80",
            },
            {
                "name": "Deluxe Double Queen",
                "code": "MIAMI_DELUXE_QUEEN",
                "description": "Spacious sanctuary for families or groups with dual queen beds and tropical garden views.",
                "base_price": 260.0,
                "total_rooms": 18,
                "max_occupancy": 4,
                "amenities": "Garden View,2 Queen Beds,Smart TV,Work Desk,Mini Bar",
                "image_url": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=1000&q=80",
            },
        ],
    },
    {
        "name": "The Grand Zenith Tower",
        "slug": "grand-zenith-tower-nyc",
        "description": "Architectural masterpiece in Midtown Manhattan offering panoramic Central Park views and white-glove service.",
        "city": "New York",
        "state": "NY",
        "country": "USA",
        "address": "550 5th Avenue, New York, NY 10036",
        "star_rating": 4.9,
        "review_score": 9.1,
        "review_count": 512,
        "image_url": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Sky Lounge,Rooftop Bar,Fitness Center,Concierge,Meeting Rooms,Pet Friendly",
        "room_types": [
            {
                "name": "Manhattan Skyline Suite",
                "code": "NYC_SKYLINE_SUITE",
                "description": "High-floor luxury suite with sprawling views of Manhattan's iconic skyline.",
                "base_price": 450.0,
                "total_rooms": 10,
                "max_occupancy": 2,
                "amenities": "Skyline View,King Bed,Executive Lounge Access,High-speed WiFi",
                "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1000&q=80",
            },
            {
                "name": "Superior City Room",
                "code": "NYC_SUPERIOR_ROOM",
                "description": "Sleek contemporary design optimized for modern business travelers and urban explorers.",
                "base_price": 290.0,
                "total_rooms": 25,
                "max_occupancy": 2,
                "amenities": "City View,Queen Bed,Ergonomic Desk,Rain Shower",
                "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=1000&q=80",
            },
        ],
    },
    {
        "name": "Zenith Garden Retreat Tokyo",
        "slug": "zenith-garden-retreat-tokyo",
        "description": "Serene Japanese garden oasis located in Roppongi, combining traditional Omotenashi hospitality with modern minimalist luxury.",
        "city": "Tokyo",
        "state": "Tokyo",
        "country": "Japan",
        "address": "6-10-1 Roppongi, Minato-ku, Tokyo 106-0032",
        "star_rating": 5.0,
        "review_score": 9.6,
        "review_count": 280,
        "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Onsen Thermal Bath,Zen Garden,Michelin Star Restaurant,Tea Ceremony Room,Airport Transfer",
        "room_types": [
            {
                "name": "Traditional Deluxe Tatami Suite",
                "code": "TOKYO_TATAMI_SUITE",
                "description": "Authentic Igusa tatami flooring, premium futon/western hybrid bedding, private hinoki cypress tub.",
                "base_price": 420.0,
                "total_rooms": 8,
                "max_occupancy": 3,
                "amenities": "Hinoki Tub,Garden View,Tea Set,Yukata Robes,Yukata Amenities",
                "image_url": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=1000&q=80",
            },
            {
                "name": "Roppongi Skyline Deluxe",
                "code": "TOKYO_SKYLINE_DELUXE",
                "description": "Sophisticated high-rise sanctuary with views of Tokyo Tower and Mount Fuji on clear days.",
                "base_price": 310.0,
                "total_rooms": 15,
                "max_occupancy": 2,
                "amenities": "Tokyo Tower View,King Bed,Bose Sound System,Air Purifier",
                "image_url": "https://images.unsplash.com/photo-1591088398332-8a7791972843?auto=format&fit=crop&w=1000&q=80",
            },
        ],
    },
    {
        "name": "Château Zenith Paris",
        "slug": "chateau-zenith-paris",
        "description": "Historic Haussmannian palace hotel along the Champs-Élysées featuring ornate frescoes and crystal chandeliers.",
        "city": "Paris",
        "state": "Île-de-France",
        "country": "France",
        "address": "28 Avenue Montaigne, 75008 Paris",
        "star_rating": 5.0,
        "review_score": 9.5,
        "review_count": 410,
        "image_url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Eiffel Tower View,Dior Spa,Champagne Bar,Sommelier Service,Courtyard Garden",
        "room_types": [
            {
                "name": "Eiffel Tower Balcony Suite",
                "code": "PARIS_EIFFEL_SUITE",
                "description": "Romantic balcony suite boasting direct, unobstructed views of the Eiffel Tower.",
                "base_price": 520.0,
                "total_rooms": 6,
                "max_occupancy": 2,
                "amenities": "Eiffel Balcony,French Breakfast Included,Hermès Toiletries,Fireplace",
                "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80",
            },
            {
                "name": "Montaigne Deluxe Room",
                "code": "PARIS_MONTAIGNE_DELUXE",
                "description": "Elegant Parisian chic room overlooking fashion houses of Avenue Montaigne.",
                "base_price": 340.0,
                "total_rooms": 14,
                "max_occupancy": 2,
                "amenities": "Street View,Queen Bed,Espresso Bar,Marble Bath",
                "image_url": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1000&q=80",
            },
        ],
    },
    {
        "name": "Zenith Alpine Lodge & Chalet",
        "slug": "zenith-alpine-lodge-aspen",
        "description": "Ski-in/ski-out luxury mountain resort in Aspen with heated outdoor pools and crackling wood-burning fireplaces.",
        "city": "Aspen",
        "state": "CO",
        "country": "USA",
        "address": "400 E Dean St, Aspen, CO 81611",
        "star_rating": 4.8,
        "review_score": 9.3,
        "review_count": 190,
        "image_url": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Ski Valet,Heated Pool,Outdoor Hot Tubs,Alpine Spa,Whiskey Lounge,Shuttle Service",
        "room_types": [
            {
                "name": "Mountain View Chalet Suite",
                "code": "ASPEN_CHALET_SUITE",
                "description": "Timber-framed alpine chalet suite with private hot tub balcony and wood fireplace.",
                "base_price": 490.0,
                "total_rooms": 8,
                "max_occupancy": 4,
                "amenities": "Wood Fireplace,Private Balcony,Ski Storage,Soaking Tub",
                "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1000&q=80",
            }
        ],
    },
]

DEMAND_EVENTS_DATA = [
    {
        "city": "Miami",
        "name": "Art Basel Miami Beach",
        "start_offset": 5,
        "duration": 4,
        "multiplier": 1.45,
    },
    {
        "city": "New York",
        "name": "NY Tech Summit & Gala",
        "start_offset": 10,
        "duration": 3,
        "multiplier": 1.35,
    },
    {
        "city": "Tokyo",
        "name": "Sakura Cherry Blossom Festival",
        "start_offset": 12,
        "duration": 7,
        "multiplier": 1.50,
    },
    {
        "city": "Paris",
        "name": "Paris Fashion Week",
        "start_offset": 18,
        "duration": 5,
        "multiplier": 1.60,
    },
]


async def seed_database():
    print("Initializing Database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        print("Seeding properties & room types...")
        created_room_types = []

        for p_data in PROPERTIES_DATA:
            room_types_data = p_data.pop("room_types")
            prop = Property(**p_data)
            session.add(prop)
            await session.flush()

            for r_data in room_types_data:
                room = RoomType(property_id=prop.id, **r_data)
                session.add(room)
                await session.flush()
                created_room_types.append(room)

        print("Seeding demand events...")
        today = date.today()
        for e_data in DEMAND_EVENTS_DATA:
            event = DemandEvent(
                city=e_data["city"],
                name=e_data["name"],
                start_date=today + timedelta(days=e_data["start_offset"]),
                end_date=today + timedelta(days=e_data["start_offset"] + e_data["duration"]),
                multiplier=e_data["multiplier"],
            )
            session.add(event)

        print("Seeding realistic sample reservations for occupancy calculations...")
        # Create some pre-existing reservations to trigger occupancy-based dynamic pricing
        sample_guests = [
            ("Alexander Wright", "alex.w@example.com"),
            ("Sophia Chen", "sophia.c@example.com"),
            ("Marcus Aurelius", "marcus.a@example.com"),
            ("Elena Rostova", "elena.r@example.com"),
        ]

        for i, room in enumerate(created_room_types):
            # Add reservations for the upcoming week
            res1 = Reservation(
                reservation_code=f"ZEN-SEED{i}A",
                room_type_id=room.id,
                guest_name=sample_guests[i % len(sample_guests)][0],
                guest_email=sample_guests[i % len(sample_guests)][1],
                check_in_date=today + timedelta(days=2),
                check_out_date=today + timedelta(days=6),
                guest_count=2,
                total_price=room.base_price * 4 * 1.2,
                night_count=4,
                status="CONFIRMED",
            )
            session.add(res1)

            # High occupancy for certain rooms
            if i % 2 == 0:
                res2 = Reservation(
                    reservation_code=f"ZEN-SEED{i}B",
                    room_type_id=room.id,
                    guest_name="David Vance",
                    guest_email="david.vance@example.com",
                    check_in_date=today + timedelta(days=3),
                    check_out_date=today + timedelta(days=7),
                    guest_count=2,
                    total_price=room.base_price * 4 * 1.35,
                    night_count=4,
                    status="CONFIRMED",
                )
                session.add(res2)

        await session.commit()
        print(
            "Database successfully seeded with realistic property, room, event, and reservation data!"
        )


if __name__ == "__main__":
    asyncio.run(seed_database())
