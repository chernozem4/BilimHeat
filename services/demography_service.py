from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from models.forecast import Forecast
from schemas.forecast import ForecastCreate, ForecastRead

class ForecastService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_forecasts(self, district_id: Optional[int] = None, year: Optional[int] = None) -> List[ForecastRead]:
        query = select(Forecast)
        if district_id is not None:
            query = query.where(Forecast.district_id == district_id)
        if year is not None:
            query = query.where(Forecast.year == year)
        result = await self.db.execute(query)
        forecasts = result.scalars().all()
        return [ForecastRead.from_orm(forecast) for forecast in forecasts]

    async def create_forecast(self, forecast_create: ForecastCreate) -> ForecastRead:
        new_forecast = Forecast(**forecast_create.dict())
        self.db.add(new_forecast)
        await self.db.commit()
        await self.db.refresh(new_forecast)
        return ForecastRead.from_orm(new_forecast)
