from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.security import get_current_active_user
from database import get_db
from models.forecast import Forecast
from schemas.forecast import ForecastCreate, ForecastRead

router = APIRouter()


@router.get("/", response_model=List[ForecastRead])
async def list_forecasts(
    district_id: Optional[int] = None,
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Получить прогнозы с возможностью фильтрации по району и году.
    """
    query = select(Forecast)
    if district_id:
        query = query.where(Forecast.district_id == district_id)
    if year:
        query = query.where(Forecast.year == year)
    result = await db.execute(query)
    forecasts = result.scalars().all()
    if not forecasts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Прогнозы не найдены")
    return forecasts


@router.post("/", response_model=ForecastRead, status_code=status.HTTP_201_CREATED)
async def create_forecast(
    forecast: ForecastCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Создать новый прогноз.
    """
    db_forecast = Forecast(**forecast.dict())
    db.add(db_forecast)
    await db.commit()
    await db.refresh(db_forecast)
    return db_forecast
