import datetime
import decimal
import enum
import os
import pathlib
import uuid
from typing import Any
from urllib import parse

import pytest

from queenbees.utils import environ, localtime


class TestEnviron:
    class SomeEnum(enum.Enum):
        VALUE1 = "value1"

    @pytest.mark.parametrize(
        "t, value, function",
        (
            (str, "test", "get_str"),
            (str, "", "get_str"),
            (int, 1, "get_int"),
            (int, 0, "get_int"),
            (bool, True, "get_bool"),
            (bool, False, "get_bool"),
            (float, 1.2, "get_float"),
            (float, 0.0, "get_float"),
            (decimal.Decimal, decimal.Decimal("1.2"), "get_decimal"),
            (decimal.Decimal, decimal.Decimal("0.0"), "get_decimal"),
            (datetime.date, datetime.date(2023, 8, 3), "get_date"),
            (datetime.time, datetime.time(1, 1, 1), "get_time"),
            (uuid.UUID, uuid.UUID(int=1), "get_uuid"),
        ),
    )
    def test_environ(self, t: type, value: Any, function: str) -> None:
        all_methods = (
            "get_str",
            "get_int",
            "get_bool",
            "get_float",
            "get_decimal",
            "get_date",
            "get_time",
            "get_uuid",
        )
        os.environ["TEST_VALUE"] = str(value)

        for m in all_methods:
            if m == function:
                returned_value = getattr(environ, function)("TEST_VALUE")

                assert returned_value == value
                assert type(returned_value) is t

            else:
                with pytest.raises(Exception):
                    getattr(environ, m)(t, value)

    def test_get_enum(self) -> None:
        os.environ["TEST_VALUE"] = "VALUE1"

        returned_value = environ.get_enum("TEST_VALUE", self.SomeEnum)

        assert returned_value == self.SomeEnum.VALUE1
        assert type(returned_value) is self.SomeEnum

    def test_get_enum_not_found(self) -> None:
        os.environ["TEST_VALUE"] = "not_value"

        with pytest.raises(Exception):
            environ.get_enum("TEST_VALUE", self.SomeEnum)

    def test_get_list(self) -> None:
        os.environ["TEST_VALUE"] = "value1,value2"

        returned_value = environ.get_list("TEST_VALUE")

        assert returned_value == ["value1", "value2"]
        assert type(returned_value) is list

    def test_get_dict(self) -> None:
        os.environ["TEST_VALUE"] = "key1=value1,key2=value2"

        returned_value = environ.get_dict("TEST_VALUE")

        assert returned_value == {"key1": "value1", "key2": "value2"}
        assert type(returned_value) is dict

    def test_get_datetime(self) -> None:
        os.environ["TEST_VALUE"] = "2023-08-06 00:00:00"

        returned_value = environ.get_datetime("TEST_VALUE")

        assert returned_value == localtime.make_aware(datetime.datetime(2023, 8, 6, 0, 0, 0))
        assert type(returned_value) is datetime.datetime
        assert returned_value.tzinfo

    def test_get_datetime_with_tz(self) -> None:
        os.environ["TEST_VALUE"] = "2023-08-06 00:00:00+00:00"

        returned_value = environ.get_datetime("TEST_VALUE")

        assert returned_value == datetime.datetime(
            2023, 8, 6, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        assert type(returned_value) is datetime.datetime
        assert returned_value.tzinfo

    def test_get_timedelta(self) -> None:
        os.environ["TEST_VALUE"] = "1"

        returned_value = environ.get_timedelta("TEST_VALUE")

        assert returned_value == datetime.timedelta(seconds=1)
        assert type(returned_value) is datetime.timedelta

    def test_get_path(self) -> None:
        os.environ["TEST_VALUE"] = "./test"

        returned_value = environ.get_path("TEST_VALUE")

        assert returned_value == pathlib.Path("./test")
        assert isinstance(returned_value, pathlib.Path)

    def test_get_url(self) -> None:
        os.environ["TEST_VALUE"] = "https://example.com"

        returned_value = environ.get_url("TEST_VALUE")

        assert returned_value.geturl() == "https://example.com"
        assert type(returned_value) is parse.ParseResult
