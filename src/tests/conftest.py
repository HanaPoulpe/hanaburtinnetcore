import configurations.wsgi
import pytest

from tests.fixtures import article, external_file, internal_file


def pytest_runtest_setup(item):  # type: ignore
    configurations.wsgi.get_wsgi_application()
