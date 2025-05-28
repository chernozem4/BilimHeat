from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Demography(Base):
    __tablename__ = "demography"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    births = Column(Integer, nullable=False)
    children_0_6 = Column(Integer, nullable=False)
    children_7_17 = Column(Integer, nullable=False)

    district = relationship("District", back_populates="demography_records")
