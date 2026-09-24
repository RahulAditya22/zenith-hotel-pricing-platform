from datetime import date, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.schemas import RoomSearchResult
from app.services.search_service import SearchService

router = APIRouter()


@router.get("", response_model=List[RoomSearchResult])
async def search_available_rooms(
    check_in_date: Optional[date] = Query(None, description="Check-in date (YYYY-MM-DD)"),
    check_out_date: Optional[date] = Query(None, description="Check-out date (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city name"),
    guests: int = Query(1, ge=1, le=10, description="Number of guests"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    sort_by: str = Query("recommended", pattern="^(recommended|price_low|price_high|rating)$"),
    db: AsyncSession = Depends(get_db),
):
    if check_in_date is None:
        check_in_date = date.today() + timedelta(days=7)
    if check_out_date is None:
        check_out_date = check_in_date + timedelta(days=3)

    if check_out_date <= check_in_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="check_out_date must be after check_in_date",
        )

    results = await SearchService.search_rooms(
        session=db,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        city=city,
        guests=guests,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
    )
    return results
