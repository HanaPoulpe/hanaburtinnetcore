import random
import string
from pathlib import Path

import pytest

from queenbees.core.content import models as content_models
from queenbees.utils import localtime
from tests.factories import content as content_factories


@pytest.fixture
def article() -> content_models.Article:
    return content_factories.Article()


@pytest.fixture
def published_article() -> content_models.Article:
    return content_factories.Article(
        published_at=localtime.now(),
    )


@pytest.fixture
def redacted_article() -> content_models.Article:
    return content_factories.Article(
        published_at=localtime.yesterday(),
        redacted_at=localtime.now(),
    )


@pytest.fixture
def internal_file(tmp_path: Path) -> content_models.File:
    return content_factories.File(
        internal_location=str(tmp_path / "".join(random.choices(string.ascii_letters, k=10)))
    )


@pytest.fixture
def external_file() -> content_models.File:
    return content_factories.File(
        external_location="https://example.com"
        + "".join(random.choices(string.ascii_letters, k=10))
    )
