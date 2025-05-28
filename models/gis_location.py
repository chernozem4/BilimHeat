from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from . import Base

class GISLocation(Base):
    __tablename__ = "gis_locations"

    id = Column(Integer, primary_key=True, index=True)
    gis_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    address = Column(String(300), nullable=True)
    latitude = Column(DOUBLE_PRECISION, nullable=True)
    longitude = Column(DOUBLE_PRECISION, nullable=True)
    type = Column(String(50), nullable=True)

