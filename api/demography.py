from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.security import get_current_active_user
from database import get_db
from models.demography import Demography
from schemas.demography import DemographyCreate, DemographyRead

router = APIRouter()


@router.get("/", response_model=List[DemographyRead])
async def list_demography(
    district_id: Optional[int] = None,
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Получить список демографических записей с возможностью фильтрации.
    """
    query = select(Demography)
    if district_id:
        query = query.where(Demography.district_id == district_id)
    if year:
        query = query.where(Demography.year == year)
    result = await db.execute(query)
    records = result.scalars().all()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данные не найдены")
    return records


@router.post("/", response_model=DemographyRead, status_code=status.HTTP_201_CREATED)
async def create_demography(
    demography: DemographyCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Создать новую демографическую запись.
    """
    db_demography = Demography(**demography.dict())
    db.add(db_demography)
    await db.commit()
    await db.refresh(db_demography)
    return db_demography
