import datetime

from django.contrib.auth import models as auth_models
from django.db import transaction

from queenbees.core.content import models as content_models
from queenbees.utils import localtime, operations


class DuplicateArticleError(operations.OperationError):
    pass


class ConflictingParametersError(operations.OperationError):
    pass


class InvalidParametersError(operations.OperationError):
    pass


@operations.operation(atomic=True)
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
    draft: content_models.ArticleDraft | None = None,
) -> content_models.Article:
    """
    Update the article match.

    :param user: User updating the article
    :param article: Existing article object
    :param name: new article title
    :param content_format: new text format, if set, new content must be provided
    :param content: new article content
    :param draft: existing draft object to use as source
    :return: updated article
    """
    if (name or content_format or content) and draft:
        raise ConflictingParametersError(
            operation_name="update_article",
            message="Cannot update article with both draft and specific values.",
        )

    if draft:
        name = draft.new_attributes.get("name", None)
        if not type(name) in (str, type(None)):
            raise TypeError("Article name must be of type str or None.")

        content_format = draft.new_attributes.get("format", None)
        if content_format:
            try:
                content_format = content_models.TextFormats(content_format)
            except KeyError:
                raise ValueError("Invalid article format.")

        content = draft.new_attributes.get("content", None)
        if not type(content) in (str, type(None)):
            raise TypeError("Article content must be of type str or None.")

        if article != draft.article:
            raise ConflictingParametersError(
                operation_name="update_article", message="Draft is not related to the article."
            )

    if content_format and not content:
        raise InvalidParametersError(
            operation_name="update_article",
            message="Article format can't be changed without changing its content.",
        )

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
            message="Failed to update article.",
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


@operations.operation(atomic=True)
def clean_content_drafts() -> None:
    """
    Delete all content drafts that are older than settings.DRAFT_EXPIRY_DAYS.
    """
    content_models.ArticleDraft.objects.expired().delete()


@operations.operation(atomic=True)
def get_or_create_article_draft(
    *,
    content: content_models.Article,
    user: auth_models.User,
) -> content_models.ArticleDraft:
    """
    Get or create a new content draft.

    :param content: Content to create a draft for
    :param user: User creating the draft
    :return: the draft
    :raise operations.OperationError: Impossible to create a draft with those data.
    """
    try:
        try:
            return content_models.ArticleDraft.objects.filter(
                content=content,
                created_by=user,
            )
        except content_models.ArticleDraft.DoesNotExist:
            return content_models.ArticleDraft.objects.create(
                content=content,
                created_by=user,
                new_attributes={},
            )
    except Exception as err:
        raise operations.OperationError(
            operation_name="get_or_create_draft",
            message="Failed to create draft.",
        ) from err
