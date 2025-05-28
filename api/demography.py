from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_current_active_user
from database import get_db
from schemas.demography import DemographyCreate, DemographyRead
from services.demography_service import DemographyService

router = APIRouter()

@router.get("/", response_model=List[DemographyRead])
async def list_demography(
    district_id: Optional[int] = None,
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = DemographyService(db)
    records = await service.list_demography(district_id=district_id, year=year)
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No demography records found")
    return records

@router.post("/", response_model=DemographyRead, status_code=status.HTTP_201_CREATED)
async def create_demography(
    demography: DemographyCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = DemographyService(db)
    new_record = await service.create_demography(demography)
    return new_record
