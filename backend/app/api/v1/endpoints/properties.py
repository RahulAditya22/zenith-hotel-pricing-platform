"""Property listing and room detail endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.domain import Property
from app.schemas.schemas import PropertyResponse, RoomTypeResponse

router = APIRouter()


@router.get("", response_model=list[PropertyResponse])
async def list_properties(
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Property).order_by(
        Property.star_rating.desc(),
    )
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get(
    "/{property_id}",
    response_model=PropertyResponse,
)
async def get_property(
    property_id: int,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Property).where(
        Property.id == property_id,
    )
    res = await db.execute(stmt)
    prop = res.scalar_one_or_none()
    if not prop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )
    return prop


@router.get(
    "/{property_id}/rooms",
    response_model=list[RoomTypeResponse],
)
async def list_property_rooms(
    property_id: int,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Property)
        .options(selectinload(Property.room_types))
        .where(Property.id == property_id)
    )
    res = await db.execute(stmt)
    prop = res.scalar_one_or_none()
    if not prop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )
    return prop.room_types
