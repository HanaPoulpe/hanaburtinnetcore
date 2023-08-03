import pytest
import time_machine

from hanaburtincore.content import models


@time_machine.travel("2023-08-03")
def test_default_article(article: models.Article) -> None:
    assert not article.is_published
    assert not article.is_redacted


@time_machine.travel("2023-08-03")
def test_published_article(published_article: models.Article) -> None:
    assert published_article.is_published
    assert not published_article.is_redacted


@time_machine.travel("2023-08-03")
def test_redacted_article(redacted_article: models.Article) -> None:
    assert not redacted_article.is_published
    assert redacted_article.is_redacted
    assert redacted_article.published_at is not None
