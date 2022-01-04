from datetime import date, datetime, timedelta
from functools import lru_cache
from json import loads
from typing import Dict, List, Optional

import config
from bson import json_util
from db.db import database
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from models.confirmed_model import Confirmed, ConfirmedByDate


@lru_cache()
def get_settings():
    return config.Settings()


settings = get_settings()

router = APIRouter(
    prefix="/cases",
    tags=["cases_confirmed"],
    responses={404: {"description": "Not found"}},
)

db = database[str(settings.mongo_col)]


@router.get(
    "/last/{country}",
    tags=["cases_confirmed"],
    summary="Get last confirmed data for a specified country",
    response_model=Confirmed,
)
def get_last_confirmed_country(country: str) -> Dict:
    """
    This function get the last day saved on mongodb and show us the confirmed cases by the country specified.
    - The country is the only needed path parameter.
    """
    date = (
        db.find({"country": country}, {"date": 1, "_id": 0}).sort("date", -1).limit(1)
    )
    date = list(date)
    if not date:
        raise HTTPException(status_code=404, detail="Country not found")
    pipeline = [
        {
            "$match": {
                "$and": [{"date": {"$eq": date[0]["date"]}}, {"country": country}]
            }
        },
        {
            "$group": {
                "_id": "",
                "cases_accumulated": {"$sum": "$cases_accumulated"},
                "cases": {"$sum": "$cases"},
            }
        },
        {"$project": {"cases": 1, "cases_accumulated": 1, "_id": 0}},
    ]
    result = db.aggregate(pipeline)
    return loads(json_util.dumps(list(result)[0]))


@router.get(
    "/date",
    tags=["cases_confirmed"],
    summary="Get the cases data for a specified country and date",
    response_model=ConfirmedByDate,
    response_model_exclude_unset=True,
)
def get_confirmed_date(date: date, countries: Optional[str] = None) -> Dict:
    """
    This function get a day and a list of countries (optional) on mongodb and show us the cases for that date.
    - The date has the following format: YYYY-MM-DD
    - The countries are optional and you can put any on them separated by (;). Example "Canada;China"
    """
    date = datetime.combine(date, datetime.min.time())
    pipeline = [
        {"$project": {"country": 1, "cases": 1, "cases_accumulated": 1}},
        {
            "$group": {
                "_id": "$country",
                "cases_accumulated": {"$sum": "$cases_accumulated"},
                "cases": {"$sum": "$cases"},
            }
        },
        {"$project": {"_id": 0, "cases": 1, "cases_accumulated": 1, "country": "$_id"}},
    ]
    if countries:
        countries = countries.split(";")
        matcher = {
            "$match": {
                "$and": [{"date": {"$in": [date]}}, {"country": {"$in": countries}}]
            }
        }
    else:
        matcher = {"$match": {"date": {"$in": [date]}}}
    pipeline.insert(0, matcher)
    result = db.aggregate(pipeline)
    result = {"countries": list(result)}
    return loads(json_util.dumps(result))


@router.get(
    "/daterange",
    tags=["cases_confirmed"],
    summary="Get the cases data for a specified country and date range or interval",
    response_model=List[Confirmed],
    response_model_exclude_unset=True,
)
def get_confirmed_daterange(
    start_date: date,
    end_date: Optional[date] = None,
    interval: Optional[int] = 15,
    countries: Optional[str] = None,
) -> Dict:
    """
    This function get a start_day, a end_date, an interval (15 days by default) and a list of countries (optional)
    on mongodb and show us the cases for that date range.
    - The start_date and end_date has the following format: YYYY-MM-DD
    - The interval count the days from the start_date
    - The countries are optional and you can put any on them separated by (;). Example "Canada;China"
    """
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date_ = datetime.combine(
        start_date + timedelta(days=interval), datetime.min.time()
    )
    if end_date:
        end_date_ = datetime.combine(end_date, datetime.min.time())
    if not countries and (end_date_ - start_date).days > 60:
        raise HTTPException(status_code=400, details="Bad request")
    pipeline = [
        {
            "$project": {
                "cases": 1,
                "cases_accumulated": 1,
                "country": 1,
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
            }
        },
        {
            "$group": {
                "_id": {"country": "$country", "date": "$date"},
                "cases_accumulated": {"$sum": "$cases_accumulated"},
                "cases": {"$sum": "$cases"},
            }
        },
        {
            "$project": {
                "country": "$_id.country",
                "date": "$_id.date",
                "cases": 1,
                "cases_accumulated": 1,
                "_id": 0,
            }
        },
    ]
    if countries:
        countries = countries.split(";")
        matcher = {
            "$match": {
                "$and": [
                    {"date": {"$lte": end_date_, "$gte": start_date}},
                    {"country": {"$in": countries}},
                ]
            }
        }
    else:
        matcher = {"$match": {"date": {"$lte": end_date_, "$gte": start_date}}}
    pipeline.insert(0, matcher)
    results = db.aggregate(pipeline)
    return loads(json_util.dumps(list(results)))


@router.get(
    "/map/{country}",
    tags=["cases_confirmed"],
    summary="Get the recovery data for a specified country and a date.",
    response_model=List[Confirmed],
    response_model_exclude_unset=True,
)
def get_confirmed_coord(country: str, date: date) -> Dict:
    """
    This function get a date and a list of country on mongodb and show us
    the cases for that date on a country with lat and long.
    - The start_date and end_date has the following format: YYYY-MM-DD
    - The country or continent.
    """

    date = datetime.combine(date, datetime.min.time())
    results = db.find(
        {"country": country, "date": date},
        {"country": 1, "cases_accumulated": 1, "_id": 0, "longitude": 1, "latitude": 1},
    )
    return loads(json_util.dumps(list(results)))
