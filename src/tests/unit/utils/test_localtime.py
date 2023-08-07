import zoneinfo
from datetime import datetime

import pytest
import time_machine
from django.test import override_settings

from hanaburtincore.utils import localtime


def assert_timezone_aware(d: localtime.datetime) -> None:
    assert d.tzinfo


@pytest.mark.parametrize("tz_name", ["UTC", "Europe/Paris"])
@time_machine.travel("2023-07-19")
def test_get_tz(tz_name: str) -> None:
    with override_settings(TIME_ZONE=tz_name):
        assert localtime.get_tz() == zoneinfo.ZoneInfo(tz_name)


@pytest.mark.parametrize("tz_name", ["UTC", "Europe/Paris"])
@time_machine.travel("2023-07-19")
def test_now(tz_name: str) -> None:
    with override_settings(TIME_ZONE=tz_name):
        now = localtime.now()

        assert_timezone_aware(now)
        assert now.tzinfo.utcoffset(now) == zoneinfo.ZoneInfo(tz_name).utcoffset(
            datetime(2023, 7, 19)
        )


@time_machine.travel("2023-08-03", tick=False)
def test_yesterday() -> None:
    now = localtime.now()

    yesterday = localtime.yesterday()

    assert_timezone_aware(yesterday)
    assert yesterday == now - localtime.timedelta(days=1)


@time_machine.travel("2023-08-06")
def test_make_aware() -> None:
    now = localtime.datetime.now()

    now = localtime.make_aware(now)

    assert_timezone_aware(now)
