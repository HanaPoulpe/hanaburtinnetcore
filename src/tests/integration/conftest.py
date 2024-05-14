from collections.abc import Iterable

import pytest


def pytest_collection_modifyitems(items: Iterable[pytest.Item]) -> None:
    for item in items:
        item.add_marker("django_db")
