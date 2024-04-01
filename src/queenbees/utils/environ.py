import datetime
import decimal
import enum
import pathlib
import uuid
from typing import Any, TypeVar
from urllib import parse

import environs

from queenbees.utils import localtime

_env = environs.Env()
_env.read_env()


def get_str(key: str, default: str | None = None) -> str:
    return _env.str(key, default=default)


def get_int(key: str, default: int | None = None) -> int:
    return _env.int(key, default=default)


def get_bool(key: str, default: bool | None = None) -> bool:
    return _env.bool(key, default=default)


def get_float(key: str, default: float | None = None) -> float:
    return _env.float(key, default=default)


def get_list(key: str, default: list[str] | None = None) -> list[str]:
    return _env.list(key, default=default)


def get_dict(key: str, default: dict[str, Any] | None = None) -> dict[str, str]:
    try:
        return _env.dict(key)
    except Exception as err:
        if default is not None:
            return default

        raise


def get_decimal(key: str, default: decimal.Decimal | None = None) -> decimal.Decimal:
    return _env.decimal(key, default=default)


def get_date(key: str, default: datetime.date | None = None) -> datetime.date:
    return _env.date(key, default=default)


def get_datetime(key: str, default: datetime.datetime | None = None) -> datetime.datetime:
    return localtime.make_aware(_env.datetime(key, default=default))


def get_time(key: str, default: datetime.time | None = None) -> datetime.time:
    return _env.time(key, default=default)


def get_timedelta(key: str, default: datetime.timedelta | None = None) -> datetime.timedelta:
    return _env.timedelta(key, default=default)


def get_url(key: str, default: str | None = None) -> parse.ParseResult:
    return _env.url(key, default=default)


def get_uuid(key: str, default: uuid.UUID | None = None) -> uuid.UUID:
    return _env.uuid(key, default=default)


def get_path(key: str, default: pathlib.Path | None = None) -> pathlib.Path:
    return _env.path(key, default=default)


_E = TypeVar("_E", bound=enum.Enum)


def get_enum(key: str, source_enum: type[_E], default: _E | None = None) -> _E:
    try:
        return _env.enum(key, type=source_enum)
    except Exception as err:
        if default:
            return default

        raise
