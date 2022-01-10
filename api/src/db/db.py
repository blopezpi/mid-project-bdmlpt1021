from functools import lru_cache

import config
from pymongo import MongoClient


@lru_cache()
def get_settings():
    return config.Settings()


settings = get_settings()

client = MongoClient(str(settings.mongo_uri))
database = client.get_database(str(settings.mongo_db))
