from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.security import get_current_active_user
from database import get_db
from models.school import School
from schemas.school import SchoolCreate, SchoolRead
from services.schools_service import SchoolsService

router = APIRouter()

@router.get("/", response_model=List[SchoolRead])
async def list_schools(
    district_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Получить список школ с фильтром по району (опционально).
    """
    service = SchoolsService(db)
    schools = await service.list_schools(district_id=district_id)
    if not schools:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Школы не найдены")
    return schools

@router.post("/", response_model=SchoolRead, status_code=status.HTTP_201_CREATED)
async def create_school(
    school_create: SchoolCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Создать новую школу.
    """
    service = SchoolsService(db)
    new_school = await service.create_school(school_create)
    return new_school
