"""Pydantic v2 request/response schemas."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# ── Property ──────────────────────────────────────────


class PropertyBase(BaseModel):
    name: str = Field(
        ...,
        json_schema_extra={
            "example": "Zenith Grand Resort & Spa",
        },
    )
    description: str = Field(
        ...,
        json_schema_extra={
            "example": (
                "Luxury oceanfront resort"
                " with top-tier amenities."
            ),
        },
    )
    city: str = Field(
        ..., json_schema_extra={"example": "Miami"},
    )
    state: Optional[str] = Field(
        None, json_schema_extra={"example": "FL"},
    )
    country: str = Field(
        "USA", json_schema_extra={"example": "USA"},
    )
    address: str = Field(
        ...,
        json_schema_extra={"example": "100 Ocean Drive"},
    )
    star_rating: float = Field(5.0, ge=1.0, le=5.0)
    review_score: float = Field(9.2, ge=1.0, le=10.0)
    review_count: int = Field(150, ge=0)
    image_url: str = Field(
        ...,
        json_schema_extra={
            "example": (
                "https://images.unsplash.com/"
                "photo-1566073771259-6a8506099945"
            ),
        },
    )
    amenities: str = Field(
        "WiFi,Pool,Spa,Gym,Restaurant",
    )


class PropertyCreate(PropertyBase):
    slug: str


class PropertyResponse(PropertyBase):
    id: int
    slug: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Room Type ─────────────────────────────────────────


class RoomTypeBase(BaseModel):
    name: str = Field(
        ...,
        json_schema_extra={
            "example": "Deluxe Ocean Suite",
        },
    )
    code: str = Field(
        ...,
        json_schema_extra={"example": "DELUXE_OCEAN"},
    )
    description: str = Field(
        ...,
        json_schema_extra={
            "example": (
                "Spacious suite with floor-to-ceiling"
                " sea views."
            ),
        },
    )
    base_price: float = Field(
        ..., gt=0, json_schema_extra={"example": 250.00},
    )
    total_rooms: int = Field(
        ..., gt=0, json_schema_extra={"example": 10},
    )
    max_occupancy: int = Field(
        2, gt=0, json_schema_extra={"example": 2},
    )
    amenities: str = Field(
        "Balcony,King Bed,Sea View,Mini Bar",
    )
    image_url: str = Field(
        ...,
        json_schema_extra={
            "example": (
                "https://images.unsplash.com/"
                "photo-1582719478250-c89cae4dc85b"
            ),
        },
    )


class RoomTypeCreate(RoomTypeBase):
    property_id: int


class RoomTypeResponse(RoomTypeBase):
    id: int
    property_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Pricing Breakdown ─────────────────────────────────


class PricingBreakdown(BaseModel):
    date: date
    base_price: float
    final_price: float
    occupancy_rate: float
    occupancy_multiplier: float
    days_to_checkin: int
    lead_time_multiplier: float
    is_weekend: bool
    weekend_multiplier: float
    demand_event_name: Optional[str] = None
    demand_event_multiplier: float = 1.0
    total_multiplier: float
    explanation: str


# ── Search Results ────────────────────────────────────


class RoomSearchResult(BaseModel):
    property_id: int
    property_name: str
    property_city: str
    star_rating: float
    review_score: float
    review_count: int
    property_image_url: str
    property_amenities: list[str]

    room_type_id: int
    room_name: str
    room_code: str
    room_image_url: str
    max_occupancy: int
    total_rooms: int
    available_rooms: int

    total_price: float
    average_nightly_price: float
    base_nightly_price: float
    value_score: float

    nightly_breakdown: list[PricingBreakdown]


# ── Reservation ───────────────────────────────────────


class ReservationCreate(BaseModel):
    room_type_id: int = Field(..., gt=0)
    guest_name: str = Field(..., min_length=2)
    guest_email: EmailStr = Field(
        ...,
        json_schema_extra={
            "example": "guest@example.com",
        },
    )
    check_in_date: date
    check_out_date: date
    guest_count: int = Field(1, gt=0)


class ReservationResponse(BaseModel):
    id: int
    reservation_code: str
    room_type_id: int
    guest_name: str
    guest_email: str
    check_in_date: date
    check_out_date: date
    guest_count: int
    total_price: float
    night_count: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Price Trend ───────────────────────────────────────


class PriceTrendPoint(BaseModel):
    date: date
    day_name: str
    is_weekend: bool
    price: float
    base_price: float
    occupancy_rate: float
    occupancy_multiplier: float
    lead_time_multiplier: float
    event_multiplier: float
    event_name: Optional[str] = None


class PriceTrendResponse(BaseModel):
    property_id: int
    property_name: str
    room_type_id: int
    room_name: str
    base_price: float
    start_date: date
    end_date: date
    points: list[PriceTrendPoint]
