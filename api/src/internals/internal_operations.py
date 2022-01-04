from functools import lru_cache

import config
from bson.objectid import ObjectId
from db.db import database
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey, APIKeyHeader
from models.internals_model import Ack, Create, Update
from utils.functutils import (
    responses_created,
    responses_deleted,
    responses_updated,
    validate_objectid,
)


@lru_cache()
def get_settings():
    return config.Settings()


settings = get_settings()

API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.api_key:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials.")


router = APIRouter(
    prefix="/internals",
    tags=["internals"],
)

db = database[str(settings.mongo_col)]


@router.delete(
    "/covid/delete/{objectid}",
    summary="Delete an object from the database",
    tags=["internals"],
    response_model=Ack,
    response_model_exclude_unset=True,
    responses=responses_deleted,
)
def delete_row(
    objectid: str = Depends(validate_objectid), api_key: APIKey = Depends(get_api_key)
):
    """
    This endpoint have the capacity for deleting an item you only must to provide a valid objectid.
    """
    if objectid:
        result = db.delete_one({"_id": ObjectId(objectid)})
        content = {}
        if result.deleted_count > 0:
            content["status"] = "Item deleted successfully"
            return JSONResponse(status_code=status.HTTP_200_OK, content=content)
        else:
            content["status"] = "Can't delete item"
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)
    else:
        raise HTTPException(status_code=400)


@router.patch(
    "/covid/update/{objectid}",
    summary="Update an object from the database",
    tags=["internals"],
    response_model=Ack,
    response_model_exclude_unset=True,
    responses=responses_updated,
)
def update_row(
    item: Update,
    objectid: str = Depends(validate_objectid),
    api_key: APIKey = Depends(get_api_key),
):
    """
    This endpoint have the capacity for updating an item you must to provide a valid objectid
    and a body parameter.
    """
    if objectid:
        result = db.update_one(
            {"_id": ObjectId(objectid)}, {"$set": item.dict(exclude_unset=True)}
        )
        content = {}
        if result.modified_count > 0:
            content["status"] = "Item updated successfully"
            return JSONResponse(status_code=status.HTTP_200_OK, content=content)
        else:
            content["status"] = "Can't update item"
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)
    else:
        raise HTTPException(status_code=400)


@router.put(
    "/covid/create",
    summary="Create an object on the database",
    tags=["internals"],
    response_model=Ack,
    response_model_exclude_unset=True,
    responses=responses_created,
)
def create_row(item: Create, api_key: APIKey = Depends(get_api_key)):
    """
    This endpoint have the capacity for creating an item you only must to provide a valid objectid
    and a body parameter.
    """
    find = db.find_one(item.dict())
    if not find:
        result = db.insert_one(item.dict())
        if result.inserted_id:
            content = {"status": "Item created successfully"}
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
    else:
        raise HTTPException(status_code=409)
