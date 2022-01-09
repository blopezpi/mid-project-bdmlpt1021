from datetime import date, datetime
from functools import lru_cache
from json import loads
from typing import Dict, List

import config
from bson import json_util
from db.db import database
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from utils.time_response import TimedRoute


@lru_cache()
def get_settings():
    return config.Settings()


settings = get_settings()

router = APIRouter(
    tags=["covid-common"],
    responses={404: {"description": "Not found"}},
    route_class=TimedRoute,
)
db = database[str(settings.mongo_col)]


@router.get("/list/countries", summary="Get all countries", tags=["covid-common"])
def list_countries() -> List[str]:
    """
    This endpoint get all the countries that we have data.
    """
    countries = db.find({}, {"country": 1, "_id": 0}).distinct("country")
    return [country for country in list(countries)]


@router.get(
    "/daterange",
    tags=["covid-common"],
    summary="Get the all data for a specified country and date range or interval",
)
def get_daterange(
    start_date: date,
    end_date: date = None,
    countries: str = None,
) -> Dict:
    """
    This function get a start_day, a end_date, an interval (15 days by default) and a list of countries
    on mongodb and show us the all for that date range.
    - The start_date and end_date has the following format: YYYY-MM-DD
    - The countries are optional and you can put any on them separated by (;). Example "Canada;China"
    """
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.min.time())

    if not countries and (end_date - start_date).days > 60:
        raise HTTPException(status_code=400, detail="Bad request")
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Bad request")
    pipeline = [
        {
            "$project": {
                "recoveries": 1,
                "recoveries_accumulated": 1,
                "cases": 1,
                "cases_accumulated": 1,
                "deaths": 1,
                "deaths_accumulated": 1,
                "country": 1,
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
            }
        },
        {
            "$group": {
                "_id": {"country": "$country", "date": "$date"},
                "recoveries_accumulated": {"$sum": "$recoveries_accumulated"},
                "recoveries": {"$sum": "$recoveries"},
                "deaths_accumulated": {"$sum": "$deaths_accumulated"},
                "deaths": {"$sum": "$deaths"},
                "cases_accumulated": {"$sum": "$cases_accumulated"},
                "cases": {"$sum": "$cases"},
            }
        },
        {
            "$project": {
                "country": "$_id.country",
                "date": "$_id.date",
                "recoveries": 1,
                "recoveries_accumulated": 1,
                "cases": 1,
                "cases_accumulated": 1,
                "deaths": 1,
                "deaths_accumulated": 1,
                "_id": 0,
            }
        },
    ]
    if countries:
        countries = countries.split(";")
        matcher = {
            "$match": {
                "$and": [
                    {"date": {"$lte": end_date, "$gte": start_date}},
                    {"country": {"$in": countries}},
                ]
            }
        }
    else:
        matcher = {"$match": {"date": {"$lte": end_date, "$gte": start_date}}}
    pipeline.insert(0, matcher)
    results = db.aggregate(pipeline)
    return loads(json_util.dumps(list(results)))
