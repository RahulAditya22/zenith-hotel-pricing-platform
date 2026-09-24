from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.schemas import PriceTrendResponse
from app.services.search_service import SearchService

router = APIRouter()


@router.get("/trend", response_model=PriceTrendResponse)
async def get_price_trend_projection(
    room_type_id: int = Query(..., gt=0, description="RoomType ID"),
    days: int = Query(30, ge=7, le=90, description="Number of days to project"),
    start_date: Optional[date] = Query(
        None, description="Start date for trend (defaults to today)"
    ),
    db: AsyncSession = Depends(get_db),
):
    try:
        trend = await SearchService.get_price_trend(
            session=db, room_type_id=room_type_id, days=days, start_date=start_date
        )
        return trend
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
