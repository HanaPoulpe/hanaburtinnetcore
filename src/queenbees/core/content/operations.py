import datetime

from django.contrib.auth import models as auth_models
from django.db import transaction

from queenbees.core.content import models as content_models
from queenbees.utils import localtime, operations


class DuplicateArticleError(operations.OperationError):
    pass


def create_article(
    *,
    name: str,
    content_format: content_models.TextFormats,
    content: str,
    user: auth_models.User | None,
) -> content_models.Article:
    """
    Create a new article in the database.

    :param name: Article title
    :param content_format: Article text format
    :param content: Article content
    :param user: User creating the article
    :return: the new article
    :raise operations.OperationError: Impossible to create an article with those data.
    """
    try:
        with transaction.atomic():
            return content_models.Article.objects.create(
                name=name,
                format=content_format,
                content=content,
                created_by=user,
                updated_by=user,
            )
    except Exception as err:
        if content_models.Article.objects.filter(name=name).exists():
            raise DuplicateArticleError(
                operation_name="create_article",
                message="Article %(name)s already exists." % {"name": name},
            ) from err
        raise operations.OperationError(
            "create_article",
            message="Failed to create article.",
        ) from err


@operations.operation(atomic=True)
def update_article(
    *,
    user: auth_models.User | None,
    article: content_models.Article,
    name: str | None = None,
    content_format: content_models.TextFormats | None = None,
    content: str | None = None,
) -> content_models.Article:
    """
    Update the article match.

    :param user: User updating the article
    :param article: Existing article object
    :param name: new article title
    :param content_format: new text format, if set, new content must be provided
    :param content: new article content
    :return: updated article
    """
    if content_format and not content:
        raise ValueError("Article format can't be changed without changing its content.")

    article.updated_by = user
    if name:
        article.name = name
    if content_format:
        article.format = content_format
    if content:
        article.content = content

    try:
        article.save()
    except Exception as err:
        raise operations.OperationError(
            operation_name="update_article",
            message="Failsed to update article.",
        ) from err
    return article


@operations.operation(atomic=True)
def publish_article(
    *,
    article: content_models.Article,
    user: auth_models.User | None,
    publication_date: datetime.datetime | None = None,
) -> content_models.Article:
    """
    Publish a new article.

    :param article: Article to publish
    :param user: User publishing the article
    :param publication_date: Publication date or None for now
    :return: published article
    :raise operations.OperationError: Operation is not possible.
    """
    if article.is_published:
        raise operations.OperationError(
            operation_name="publish_article",
            message="Article is already published.",
        )
    if article.is_redacted:
        raise operations.OperationError(
            operation_name="publish_article",
            message="Article have been redacted.",
        )

    article.updated_by = user
    article.published_at = publication_date or localtime.now()

    try:
        article.save()
    except Exception as err:
        raise operations.OperationError(
            operation_name="publish_article",
            message="Failed to publish article.",
        ) from err

    return article


@operations.operation(atomic=True)
def redact_article(
    *,
    article: content_models.Article,
    user: auth_models.User | None,
    redaction_date: datetime.datetime | None = None,
) -> content_models.Article:
    """
    Redact an article.

    :param article: article to redact
    :param user: User redacting the article
    :param redaction_date: Effective redaction date, None for now
    :return: redacted article
    :raise operations.OperationError: Operation is not possible
    :raise ValueError: Parameters are not valid.
    """
    if not article.is_published:
        raise operations.OperationError(
            operation_name="redact_article",
            message="Cannot redact an unpublished article.",
        )
    if article.is_redacted:
        raise operations.OperationError(
            operation_name="redact_article",
            message="Article is already redacted.",
        )
    if redaction_date and article.published_at > redaction_date:
        raise ValueError("Article cannot be redacted before its publication.")

    article.updated_by = user
    article.redacted_at = redaction_date or localtime.now()
    article.save()

    return article
