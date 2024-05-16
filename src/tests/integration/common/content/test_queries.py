import pytest
import time_machine

from queenbees.core.content import models, queries
from tests.types import ArticleDraftFixture


class TestArticleQueries:
    @pytest.fixture(autouse=True)
    def set_time(
        self, time_machine: time_machine.TimeMachineFixture
    ) -> time_machine.TimeMachineFixture:
        time_machine.move_to("2023-08-05 00:00:00", tick=False)
        return time_machine

    def test_get_article_by_name(self, article: models.Article) -> None:
        article_name = article.name

        found_article = queries.get_article_by_name(article_name)

        assert article == found_article

    def test_published_queryset(
        self,
        published_article: models.Article,
        redacted_article: models.Article,
        article: models.Article,
    ) -> None:
        answer = [a for a in models.Article.objects.published()]

        assert [published_article] == answer

    def test_redacted_queryset(
        self,
        published_article: models.Article,
        redacted_article: models.Article,
        article: models.Article,
    ) -> None:
        answer = [a for a in models.Article.objects.redacted()]

        assert [redacted_article] == answer

    def test_draft_articles(
        self,
        published_article: models.Article,
        redacted_article: models.Article,
        article: models.Article,
    ) -> None:
        answer = [a for a in models.Article.objects.draft()]

        assert [article] == answer


class TestContentDraftQueries:
    def test_expired_drafts(
        self,
        expired_article_draft: ArticleDraftFixture,
        article_draft: ArticleDraftFixture,
    ) -> None:
        all_expired_drafts = models.ArticleDraft.objects.expired()

        assert expired_article_draft.draft in all_expired_drafts
        assert article_draft.draft not in all_expired_drafts
