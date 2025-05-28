from pydantic import BaseModel
from typing import Optional

class DistrictBase(BaseModel):
    name: str
    gis_id: Optional[str] = None

class DistrictCreate(DistrictBase):
    pass

class DistrictRead(DistrictBase):
    id: int

    class Config:
        orm_mode = True
