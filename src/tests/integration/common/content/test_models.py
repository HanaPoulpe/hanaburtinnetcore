import attr
import pytest
import time_machine

from queenbees.core.content import models, operations
from tests import factories


@attr.define(frozen=True)
class ArticleStatus:
    status: models.Article.Status
    article: models.Article


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

    @pytest.fixture
    def article_with_status(
        self,
        request: pytest.FixtureRequest,
        article: models.Article,
    ) -> ArticleStatus:
        if request.param == "published":
            return ArticleStatus(
                models.Article.Status.PUBLISHED,
                operations.publish_article(
                    article=article,
                    user=None,
                ),
            )

        if request.param == "redacted":
            operations.publish_article(
                article=article,
                user=None,
            )
            return ArticleStatus(
                models.Article.Status.REDACTED,
                operations.redact_article(
                    article=article,
                    user=None,
                ),
            )

        return ArticleStatus(
            models.Article.Status.DRAFT,
            article,
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "article_with_status",
        ["draft", "published", "redacted"],
        indirect=True,
    )
    def test_article_status(self, article_with_status: ArticleStatus) -> None:
        assert article_with_status.article.status == article_with_status.status


class TestArticleDraft:
    def change_article_name_to_duplicate(
        self,
        article_draft: models.ArticleDraft,
        article: models.Article,
    ) -> None:
        with pytest.raises(models.ArticleDraft.ArticleNameAlreadyUsedException):
            article_draft.set_attributes(
                {
                    "name": article.name,
                }
            )
