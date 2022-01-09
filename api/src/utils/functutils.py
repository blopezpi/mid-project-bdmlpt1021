from datetime import datetime

from bson import ObjectId


def validate_objectid(objectid):
    return ObjectId(objectid) if ObjectId.is_valid(objectid) else False


responses_internals = {
    403: {"description": "Not enough privileges"},
}

responses_created = {
    **responses_internals,
    409: {"description": "Element already exists"},
    201: {"description": "Created"},
}

responses_updated = {
    **responses_internals,
    400: {"description": "Bad request"},
    404: {"description": "Element not found"},
    200: {"description": "Updated"},
}

responses_deleted = {
    **responses_internals,
    400: {"description": "Bad request"},
    404: {"description": "Element not found"},
    200: {"description": "Deleted"},
}

responses = {
    404: {"description": "Item not found"},
    200: {"description": "OK"},
}


def validate_month(date_: str):
    return datetime.strptime(date_, "%Y-%m")
