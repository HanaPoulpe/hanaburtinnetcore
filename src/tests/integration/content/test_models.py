import pytest
import time_machine

from queenbees.core.content import models


class TestArticle:
    @pytest.fixture(autouse=True)
    def set_time(self, time_machine: time_machine.TimeMachineFixture) -> None:
        time_machine.move_to("2023-08-03")

    @pytest.mark.django_db
    def test_default_article(self, article: models.Article) -> None:
        assert not article.is_published
        assert not article.is_redacted

    @pytest.mark.django_db
    def test_published_article(self, published_article: models.Article) -> None:
        assert published_article.is_published
        assert not published_article.is_redacted

    @pytest.mark.django_db
    def test_redacted_article(self, redacted_article: models.Article) -> None:
        assert not redacted_article.is_published
        assert redacted_article.is_redacted
        assert redacted_article.published_at is not None
