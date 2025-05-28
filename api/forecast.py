from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_current_active_user
from database import get_db
from schemas.forecast import ForecastCreate, ForecastRead
from services.forecast_service import ForecastService

router = APIRouter()

@router.get("/", response_model=List[ForecastRead])
async def list_forecasts(
    district_id: Optional[int] = None,
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = ForecastService(db)
    forecasts = await service.list_forecasts(district_id=district_id, year=year)
    if not forecasts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Прогнозы не найдены")
    return forecasts

@router.post("/", response_model=ForecastRead, status_code=status.HTTP_201_CREATED)
async def create_forecast(
    forecast: ForecastCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = ForecastService(db)
    new_forecast = await service.create_forecast(forecast)
    return new_forecast
