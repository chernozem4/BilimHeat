from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .user import User
from .district import District
from .demography import Demography
from .school import School
from .forecast import Forecast
from .gis_location import GISLocation

