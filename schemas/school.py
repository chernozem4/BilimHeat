from pydantic import BaseModel

class SchoolBase(BaseModel):
    name: str
    district_id: int
    capacity: int

class SchoolCreate(SchoolBase):
    pass

class SchoolRead(SchoolBase):
    id: int

    class Config:
        orm_mode = True
