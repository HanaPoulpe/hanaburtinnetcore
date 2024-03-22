import pytest

from queenbees.core.content import models, queries
from tests.types import ArticleDraftFixture


class TestArticleQueries:
    @pytest.mark.django_db
    def test_get_article_by_name(self, article: models.Article) -> None:
        article_name = article.name

        found_article = queries.get_article_by_name(article_name)

        assert article == found_article


class TestContentDraftQueries:
    @pytest.mark.django_db
    def test_expired_drafts(
        self,
        expired_article_draft: ArticleDraftFixture,
        article_draft: ArticleDraftFixture,
    ) -> None:
        all_expired_drafts = models.ArticleDraft.objects.expired()

        assert expired_article_draft.draft in all_expired_drafts
        assert article_draft.draft not in all_expired_drafts
