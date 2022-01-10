from datetime import date, timedelta

import requests
from config import api_uri


def range(
    type_: str, start: date, countries: str, interval: int = 15, end: date = None
):
    params = {"countries": countries}
    params["start_date"] = start
    params["end_date"] = start + timedelta(days=interval)
    if end:
        params["end_date"] = end
    if type_ == "all":
        return requests.get(f"{api_uri}/daterange", params=params).json()
    return requests.get(f"{api_uri}/{type_}/daterange", params=params).json()


def m_range(type_: str, start: str, countries: str, end: str):
    params = {"countries": countries}
    params["start_month"] = start
    params["end_month"] = end
    return requests.get(f"{api_uri}/{type_}/monthrange", params=params).json()


def last_data(type_: str, country: str = None):
    if country:
        return requests.get(f"{api_uri}/{type_}/last/{country}").json()
    return requests.get(f"{api_uri}/{type_}/last").json()


def by_date(type_: str, date: date, countries: str = None):
    params = {"date": date}
    if countries:
        params["countries"] = countries
        return requests.get(f"{api_uri}/{type_}/date", params=params).json()
    return requests.get(f"{api_uri}/{type_}", params=params).json()


def get_countries():
    return requests.get(f"{api_uri}/list/countries").json()


def get_map(type_: str, date: date):
    params = {"date": date}
    return requests.get(f"{api_uri}/{type_}/map", params=params).json()
