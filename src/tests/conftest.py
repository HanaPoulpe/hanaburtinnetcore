import configurations.wsgi
import pytest

from tests.fixtures import *


def pytest_runtest_setup(item: pytest.Item) -> None:
    configurations.wsgi.get_wsgi_application()
