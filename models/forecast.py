from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    forecast_kindergarten = Column(Integer, nullable=False)
    forecast_school = Column(Integer, nullable=False)

    district = relationship("District", back_populates="forecasts")
