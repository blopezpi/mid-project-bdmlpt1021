from typing import List, Optional

from pydantic import BaseModel


class Deaths(BaseModel):
    deaths: Optional[int]
    deaths_accumulated: Optional[int]
    country: Optional[str]
    date: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]


class DeathsByDate(BaseModel):
    countries: List[Deaths]
