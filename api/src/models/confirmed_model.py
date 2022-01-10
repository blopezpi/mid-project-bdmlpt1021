from typing import List, Optional

from pydantic import BaseModel


class Confirmed(BaseModel):
    cases: Optional[int]
    cases_accumulated: Optional[int]
    country: Optional[str]
    date: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]


class ConfirmedByDate(BaseModel):
    countries: List[Confirmed]
