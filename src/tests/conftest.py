import sys

import pytest

from tests.fixtures import *


def pytest_runtest_setup(item: pytest.Item) -> None:
    from configurations.management import execute_from_command_line
