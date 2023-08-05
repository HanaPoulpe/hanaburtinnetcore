import pytest

from hanaburtincore.content import models, queries


@pytest.mark.django_db
def test_get_article_by_name(article: models.Article) -> None:
    article_name = article.name

    found_article = queries.get_article_by_name(article_name)

    assert article == found_article
