from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.school import School
from schemas.school import SchoolCreate, SchoolRead

class SchoolsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_schools(self, district_id: Optional[int] = None) -> List[SchoolRead]:
        query = select(School)
        if district_id is not None:
            query = query.where(School.district_id == district_id)
        result = await self.db.execute(query)
        schools = result.scalars().all()
        return [SchoolRead.from_orm(school) for school in schools]

    async def create_school(self, school_create: SchoolCreate) -> SchoolRead:
        new_school = School(**school_create.dict())
        self.db.add(new_school)
        await self.db.commit()
        await self.db.refresh(new_school)
        return SchoolRead.from_orm(new_school)
