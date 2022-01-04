from functools import lru_cache
from typing import List

import config
from db.db import database
from fastapi import APIRouter


@lru_cache()
def get_settings():
    return config.Settings()


settings = get_settings()

router = APIRouter()
db = database[str(settings.mongo_col)]


@router.get("/list/countries", summary="Get all countries", tags=["covid-common"])
def list_countries() -> List[str]:
    """
    This endpoint get all the countries that we have data.
    """
    countries = db.find({}, {"country": 1, "_id": 0}).distinct("country")
    return [country for country in list(countries)]
