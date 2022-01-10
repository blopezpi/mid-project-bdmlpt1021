from functools import lru_cache

import config
from fastapi import FastAPI
from internals import internal_operations
from routers import common, confirmed_cases, deaths, recoveries


@lru_cache()
def get_settings():
    return config.Settings()


settings = get_settings()

description = """
Covid API helps you do get updated about the covid pandemic. 🚀

You can read more [here](https://github.com/blopezpi/mid-project-bdmlpt1021/blob/main/README.md)
"""

tags_metadata = [
    {
        "name": "recoveries",
        "description": "Get covid data recoveries, you have the followings endpoints.",
    },
    {
        "name": "cases_confirmed",
        "description": "Get covid data confirmed cases, you have the followings endpoints.",
    },
    {
        "name": "deaths",
        "description": "Get covid data deaths, you have the followings endpoints.",
    },
    {
        "name": "internals",
        "description": "Update, deleted, create on the database new values (Authentication required).",
    },
    {
        "name": "covid-common",
        "description": "Common endpoints for the API.",
    },
]


def create_application():
    app = FastAPI(
        title=settings.app_name,
        description=description,
        openapi_tags=tags_metadata,
        contact={
            "name": "Borja Lopez",
            "url": "https://github.com/blopezpi/mid-project-bdmlpt1021",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
    )

    app.include_router(common.router)
    app.include_router(confirmed_cases.router)
    app.include_router(deaths.router)
    app.include_router(recoveries.router)
    app.include_router(internal_operations.router)

    return app


app = create_application()


@app.on_event("startup")
def start():
    if settings.log_level == "debug":
        print(settings)


@app.on_event("shutdown")
def shutdown():
    print("Shutdown API. Bye Bye.")


@app.get("/")
def root():
    return {"message": "Welcome to the COVID 19 API"}
