import os
from enum import Enum

from pydantic import BaseSettings


class LogLevel(str, Enum):
    info = "info"
    debug = "debug"
    error = "error"
    warning = "warning"


class Settings(BaseSettings):
    app_name: str = "Covid API"
    mongo_uri: str = os.getenv("MONGO_URI")
    mongo_db: str = os.getenv("MONGO_DB")
    mongo_col: str = os.getenv("MONGO_COL")
    api_key: str = os.getenv("API_KEY")
    log_level: LogLevel = os.getenv("LOG_LEVEL", "info")

    class Config:
        if os.path.exists(".env"):
            env_prefix = ""
            env_file = ".env"
