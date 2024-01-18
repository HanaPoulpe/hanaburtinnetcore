import os.path

import configurations.wsgi
import dotenv
import pytest

from tests.fixtures import *


def pytest_runtest_setup(item: pytest.Item) -> None:
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    from configurations.management import execute_from_command_line
