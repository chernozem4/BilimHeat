from pydantic import BaseModel

class ForecastBase(BaseModel):
    district_id: int
    year: int
    forecast_kindergarten: int
    forecast_school: int

class ForecastCreate(ForecastBase):
    pass

class ForecastRead(ForecastBase):
    id: int

    class Config:
        orm_mode = True
