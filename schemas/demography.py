from pydantic import BaseModel

class DemographyBase(BaseModel):
    district_id: int
    year: int
    births: int
    children_0_6: int
    children_7_17: int

class DemographyCreate(DemographyBase):
    pass

class DemographyRead(DemographyBase):
    id: int

    class Config:
        orm_mode = True
