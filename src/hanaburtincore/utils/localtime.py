import zoneinfo
from datetime import date, datetime, time, timedelta, timezone, tzinfo
from typing import TypeVar

from django.conf import settings


def get_tz() -> tzinfo:
    return zoneinfo.ZoneInfo(settings.TIME_ZONE)


def now(tz: tzinfo | None = None) -> datetime:
    return datetime.now(tz or get_tz())


def yesterday(tz: tzinfo | None = None) -> datetime:
    return now(tz) - timedelta(days=1)


def make_aware(o: datetime) -> datetime:
    if o.tzinfo is not None:
        return o
    o = o.astimezone(tz=get_tz())

    return o
