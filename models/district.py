from sqlalchemy.orm import relationship

from app.models import Base


class District(Base):
    # ...
    demography_records = relationship("Demography", back_populates="district")
    schools = relationship("School", back_populates="district")
    forecasts = relationship("Forecast", back_populates="district")

