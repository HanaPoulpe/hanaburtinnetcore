from datetime import date, datetime, time, timedelta, timezone, tzinfo

import pytz
from django.conf import settings


def get_tz() -> tzinfo:
    return pytz.timezone(settings.TIME_ZONE)


def now(tz: tzinfo | None = None) -> datetime:
    return datetime.now(tz or get_tz())
