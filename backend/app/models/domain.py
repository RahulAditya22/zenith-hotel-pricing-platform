from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="USA")
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    star_rating: Mapped[float] = mapped_column(Float, nullable=False, default=4.5)
    review_score: Mapped[float] = mapped_column(Float, nullable=False, default=8.8)
    review_count: Mapped[int] = mapped_column(Integer, nullable=False, default=120)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    amenities: Mapped[str] = mapped_column(
        String(500), nullable=False, default="WiFi,Pool,Spa,Gym,Restaurant"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    room_types: Mapped[List["RoomType"]] = relationship(
        "RoomType", back_populates="property", cascade="all, delete-orphan"
    )
    demand_events: Mapped[List["DemandEvent"]] = relationship(
        "DemandEvent", back_populates="property", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Property(id={self.id}, name='{self.name}', city='{self.city}')>"


class RoomType(Base):
    __tablename__ = "room_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., Deluxe King Suite
    code: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., DELUXE_KING
    description: Mapped[str] = mapped_column(Text, nullable=False)
    base_price: Mapped[float] = mapped_column(Float, nullable=False)  # Base price per night in USD
    total_rooms: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # Capacity threshold for occupancy calc
    max_occupancy: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    amenities: Mapped[str] = mapped_column(
        String(500), nullable=False, default="Balcony,King Bed,City View,Mini Bar"
    )
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    property: Mapped["Property"] = relationship("Property", back_populates="room_types")
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", back_populates="room_type", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<RoomType(id={self.id}, name='{self.name}', base_price={self.base_price})>"


class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = (
        Index("idx_res_room_dates", "room_type_id", "check_in_date", "check_out_date"),
        CheckConstraint("check_out_date > check_in_date", name="chk_valid_dates"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    reservation_code: Mapped[str] = mapped_column(
        String(36), unique=True, nullable=False, index=True
    )
    room_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("room_types.id", ondelete="CASCADE"), nullable=False, index=True
    )
    guest_name: Mapped[str] = mapped_column(String(150), nullable=False)
    guest_email: Mapped[str] = mapped_column(String(150), nullable=False)
    check_in_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    check_out_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    guest_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    night_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="CONFIRMED", index=True
    )  # CONFIRMED, CANCELLED
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    room_type: Mapped["RoomType"] = relationship("RoomType", back_populates="reservations")

    def __repr__(self) -> str:
        return f"<Reservation(code='{self.reservation_code}', room_type_id={self.room_type_id}, check_in={self.check_in_date})>"


class DemandEvent(Base):
    __tablename__ = "demand_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    property_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=True, index=True
    )
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )  # e.g., Tech Conference 2026, Summer Music Fest
    start_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    multiplier: Mapped[float] = mapped_column(
        Float, nullable=False, default=1.3
    )  # e.g. 1.30 for 30% surge

    property: Mapped[Optional["Property"]] = relationship(
        "Property", back_populates="demand_events"
    )

    def __repr__(self) -> str:
        return f"<DemandEvent(name='{self.name}', multiplier={self.multiplier})>"
