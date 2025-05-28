from pydantic import BaseModel
from typing import Optional

class GISLocationBase(BaseModel):
    gis_id: str
    name: str
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    type: Optional[str]

class GISLocationCreate(GISLocationBase):
    pass

class GISLocationRead(GISLocationBase):
    id: int

    class Config:
        orm_mode = True
