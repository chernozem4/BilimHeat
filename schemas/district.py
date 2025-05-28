from pydantic import BaseModel

class DistrictBase(BaseModel):
    name: str
    gis_id: str | None = None

class DistrictCreate(DistrictBase):
    pass

class DistrictRead(DistrictBase):
    id: int

    class Config:
        orm_mode = True
