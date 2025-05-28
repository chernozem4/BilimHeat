from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    gis_id = Column(String(50), unique=True, nullable=True)

    demography_records = relationship("Demography", back_populates="district")
    schools = relationship("School", back_populates="district")
    forecasts = relationship("Forecast", back_populates="district")


