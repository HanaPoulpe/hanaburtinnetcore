import configurations.wsgi
import pytest

from tests.fixtures import *


def pytest_runtest_setup(item):  # type: ignore
    configurations.wsgi.get_wsgi_application()
