from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Location(BaseModel):
    type: Optional[str]
    coordinates: Optional[List[float]]


class Update(BaseModel):
    deaths: Optional[int]
    deaths_accumulated: Optional[int]
    cases_accumulated: Optional[int]
    cases: Optional[int]
    country: Optional[str]
    date: Optional[datetime]
    longitude: Optional[float]
    latitude: Optional[float]
    recoveries: Optional[int]
    recoveries_accumulated: Optional[int]
    location: Optional[Location]


class Create(BaseModel):
    deaths: int
    deaths_accumulated: int
    cases_accumulated: int
    cases: int
    country: str
    date: datetime
    longitude: float
    latitude: float
    recoveries: int
    recoveries_accumulated: int
    location: Location


class Ack(BaseModel):
    status: str
