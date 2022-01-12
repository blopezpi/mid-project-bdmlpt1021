import os

import sentry_sdk


def set_sentry():
    sentry_sdk.init(os.getenv("SENTRY_DSN"), environment=os.getenv("ENV", "dev"))

    sentry_sdk.set_tag("component", "DASHBOARD")
