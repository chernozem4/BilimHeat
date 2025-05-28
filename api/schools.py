from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.security import get_current_active_user
from database import get_db
from models.school import School
from schemas.school import SchoolCreate, SchoolRead

router = APIRouter()


@router.get("/", response_model=List[SchoolRead])
async def list_schools(
    district_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Получить список школ с возможностью фильтрации по району.
    """
    query = select(School)
    if district_id:
        query = query.where(School.district_id == district_id)
    result = await db.execute(query)
    schools = result.scalars().all()
    if not schools:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Школы не найдены")
    return schools


@router.post("/", response_model=SchoolRead, status_code=status.HTTP_201_CREATED)
async def create_school(
    school: SchoolCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Создать новую школу.
    """
    db_school = School(**school.dict())
    db.add(db_school)
    await db.commit()
    await db.refresh(db_school)
    return db_school
