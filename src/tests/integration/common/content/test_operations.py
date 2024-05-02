from typing import Any

import lorem
import pytest
import time_machine

from queenbees.core.content import models
from queenbees.core.content import operations as content_operations
from queenbees.utils import localtime, operations
from tests.factories import content as content_factories
from tests.types import ArticleDraftFixture


class TestArticleOperations:
    @pytest.fixture(autouse=True)
    def set_time(self, time_machine: time_machine.TimeMachineFixture) -> None:
        time_machine.move_to("2023-08-05 00:00:00", tick=False)

    @pytest.fixture
    def title(self) -> str:
        return lorem.get_sentence()[:100]

    @pytest.fixture
    def content(self) -> str:
        return lorem.get_paragraph()

    @pytest.fixture
    def published(
        self, request: Any, published_article: models.Article, redacted_article: models.Article
    ) -> models.Article:
        if request.param == "published":
            return published_article
        return redacted_article

    @pytest.fixture
    def not_published(
        self, request: Any, article: models.Article, redacted_article: models.Article
    ) -> models.Article:
        if request.param == "redacted":
            return redacted_article
        return article

    @pytest.mark.django_db
    def test_create_article(
        self,
        title: str,
        content: str,
    ) -> None:
        # TODO: Add user fixture
        article = content_operations.create_article(
            name=title,
            content_format=models.TextFormats.PLAIN_TEXT,
            content=content,
            user=None,
        )

        assert article.name == title
        assert article.content == content
        assert article.created_at == localtime.now()
        assert article.updated_at == localtime.now()

    @pytest.mark.django_db
    def test_create_duplicate_article(
        self,
        article: models.Article,
        content: str,
    ) -> None:
        with pytest.raises(content_operations.DuplicateArticleError):
            content_operations.create_article(
                name=article.name,
                content=content,
                content_format=models.TextFormats.PLAIN_TEXT,
                user=None,
            )

    @pytest.mark.django_db
    def test_update_article(
        self,
        content: str,
        article: models.Article,
        time_machine: time_machine.TimeMachineFixture,
    ) -> None:
        # TODO: Add user fixture
        original_created_at = article.created_at
        original_created_by = article.created_by

        time_machine.move_to("2023-08-06 00:00:00", tick=False)

        article = content_operations.update_article(
            user=None,
            article=article,
            content=content,
        )

        assert article.content == content
        assert original_created_by == article.created_by
        assert original_created_at == article.created_at
        assert article.updated_at == localtime.now()

    @pytest.mark.django_db
    def test_update_article_from_draft(
        self,
        article_draft: ArticleDraftFixture,
    ) -> None:
        article = content_operations.update_article(
            user=None,
            article=article_draft.article,
            draft=article_draft.draft,
        )

        assert article.content == article_draft.draft.new_attributes["content"]
        assert article.format == article_draft.draft.new_attributes["format"]
        assert article.name == article_draft.draft.new_attributes["name"]

    @pytest.mark.django_db
    def test_update_wrong_article_from_draft(
        self,
        article: models.Article,
        article_draft: ArticleDraftFixture,
    ) -> None:
        with pytest.raises(content_operations.ConflictingParametersError):
            content_operations.update_article(
                user=None,
                article=article,
                draft=article_draft.draft,
            )

    @pytest.mark.django_db
    def test_update_article_with_conflicting_parameters(
        self,
        article_draft: ArticleDraftFixture,
    ) -> None:
        with pytest.raises(content_operations.ConflictingParametersError):
            content_operations.update_article(
                user=None,
                article=article_draft.article,
                draft=article_draft.draft,
                content="Shouldn't be here!",
            )

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "content_format",
        [models.TextFormats.PLAIN_TEXT, models.TextFormats.HTML, models.TextFormats.MARKDOWN],
    )
    def test_update_article_format(
        self,
        article: models.Article,
        content: str,
        content_format: models.TextFormats,
    ) -> None:
        article = content_operations.update_article(
            user=None,
            article=article,
            content_format=content_format,
            content=content,
        )

        assert article.content == content
        assert article.format == content_format

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "content_format",
        [models.TextFormats.PLAIN_TEXT, models.TextFormats.HTML, models.TextFormats.MARKDOWN],
    )
    def test_update_article_format_without_content(
        self,
        article: models.Article,
        content_format: models.TextFormats,
    ) -> None:
        with pytest.raises(ValueError):
            content_operations.update_article(
                user=None,
                article=article,
                content_format=content_format,
            )

    @pytest.mark.django_db
    def test_publish_article(self, article: models.Article) -> None:
        article = content_operations.publish_article(
            user=None,
            article=article,
        )

        assert article.is_published

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "published",
        ("published", "redacted"),
        indirect=True,
    )
    def test_publish_published_article(self, published: models.Article) -> None:
        with pytest.raises(operations.OperationError):
            content_operations.publish_article(
                user=None,
                article=published,
            )

    @pytest.mark.django_db
    def test_redact_article(self, published_article: models.Article) -> None:
        article = content_operations.redact_article(
            user=None,
            article=published_article,
        )

        assert not article.is_published
        assert article.is_redacted

    @pytest.mark.django_db
    @pytest.mark.parametrize("not_published", ("not_published", "redacted"), indirect=True)
    def test_redact_not_redactable_article(self, not_published: models.Article) -> None:
        with pytest.raises(operations.OperationError):
            content_operations.redact_article(
                user=None,
                article=not_published,
            )

    @pytest.mark.django_db
    def test_redact_article_with_invalid_dates(self, published_article: models.Article) -> None:
        long_past = localtime.make_aware(localtime.datetime(1970, 1, 1))
        with pytest.raises(ValueError):
            content_operations.redact_article(
                user=None,
                article=published_article,
                redaction_date=long_past,
            )


class TestDraftOperations:
    @pytest.fixture(autouse=True)
    def set_time(self, time_machine: time_machine.TimeMachineFixture) -> None:
        time_machine.move_to("2024-03-19 00:00:00", tick=False)

    @pytest.mark.django_db
    def test_clean_content_drafts(
        self,
        expired_article_draft: ArticleDraftFixture,
    ) -> None:
        content_operations.clean_content_drafts()

        draft_count = models.ArticleDraft.objects.all().count()
        assert draft_count == 0
