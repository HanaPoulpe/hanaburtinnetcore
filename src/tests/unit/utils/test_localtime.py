from datetime import datetime

import pytest
import pytz
import time_machine
from django.test import override_settings

from hanaburtincore.utils import localtime


def assert_timezone_aware(d: localtime.datetime) -> None:
    assert d.tzinfo


@pytest.mark.parametrize("tz_name", ["UTC", "Europe/Paris"])
@time_machine.travel("2023-07-19")
def test_get_tz(tz_name: str) -> None:
    with override_settings(TIME_ZONE=tz_name):
        assert localtime.get_tz() == pytz.timezone(tz_name)


@pytest.mark.parametrize("tz_name", ["UTC", "Europe/Paris"])
@time_machine.travel("2023-07-19")
def test_now(tz_name: str) -> None:
    with override_settings(TIME_ZONE=tz_name):
        now = localtime.now()

        assert_timezone_aware(now)
        assert now.tzinfo.utcoffset(now) == pytz.timezone(tz_name).utcoffset(datetime(2023, 7, 19))
