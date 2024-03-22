import uuid
from typing import Self

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import models

from queenbees.core import models as core_models
from queenbees.utils import localtime


# Enums #
class TextFormats(models.TextChoices):
    PLAIN_TEXT = "PLAIN", "Plain Text"
    HTML = "HTML", "HTML"
    MARKDOWN = "MD", "Markdown"


class FileSourceTypes(models.TextChoices):
    EXTERNAL = "EXTERNAL", "File stored on an external storage"


# Models #
class GenericContent(core_models.TimeStampedMixin, core_models.UUIDIdentifierMixin, models.Model):
    name: models.CharField = models.CharField(max_length=100, blank=False, null=False, unique=True)

    created_by = models.ForeignKey(
        auth_models.User, on_delete=models.PROTECT, null=True, related_name="created_+"
    )
    updated_by = models.ForeignKey(
        auth_models.User, on_delete=models.PROTECT, null=True, related_name="maintained_+"
    )

    @property
    def url(self) -> str:
        raise NotImplementedError("Content url must be specified.")

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        return "%(class)s<id=%(id)s, name=%(name)r>" % {
            "class": self.__class__.__name__,
            "id": self.id,
            "name": self.name,
        }


class Article(GenericContent):
    format = models.CharField(max_length=30, choices=TextFormats.choices, null=False, blank=False)
    content = models.TextField()
    published_at = models.DateTimeField(null=True, default=None)
    redacted_at = models.DateTimeField(null=True, default=None)

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        REDACTED = "REDACTED", "Redacted"

    @property
    def is_published(self) -> bool:
        if not self.published_at:
            return False

        return self.published_at <= localtime.now() and not self.is_redacted

    @property
    def is_redacted(self) -> bool:
        if not self.redacted_at:
            return False

        return self.redacted_at <= localtime.now()

    @property
    def status(self) -> Status:
        if self.is_published:
            return self.Status.PUBLISHED

        if self.is_redacted:
            return self.Status.REDACTED

        return self.Status.DRAFT

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(published_at__lte=models.F("redacted_at")),
                name="check_published_redacted_dates",
            ),
            models.CheckConstraint(
                check=models.Q(published_at__isnull=False)
                | models.Q(published_at__isnull=True, redacted_at__isnull=True),
                name="check_published_if_redacted",
            ),
        ]


class File(GenericContent):
    source_type = models.CharField(
        max_length=30, choices=FileSourceTypes.choices, null=False, blank=False
    )
    internal_location = models.CharField(max_length=300, null=True, blank=False)
    external_location = models.CharField(max_length=300, null=True, blank=False)

    @property
    def public_url(self) -> str:
        return self.external_location or settings.BROKEN_MEDIA_URL  # type: ignore


class ArticleDraftQuerySet(models.QuerySet["ArticleDraft"]):
    def expired(self) -> Self:
        return self.filter(
            updated_at__lte=localtime.now() - localtime.timedelta(days=settings.DRAFT_EXPIRY_DAYS)
        )


class ArticleDraft(core_models.TimeStampedMixin, models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="drafts")

    working_user: auth_models.User = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)

    new_attributes = models.JSONField(null=False)

    class Meta:
        indexes = [
            models.Index(fields=["updated_at"]),
            models.Index(fields=["article", "working_user"]),
        ]

    objects = ArticleDraftQuerySet.as_manager()

    @property
    def expiry_date(self) -> localtime.datetime:
        return self.updated_at + localtime.timedelta(days=settings.DRAFT_EXPIRY_DAYS)

    @property
    def is_expired(self) -> bool:
        return self.expiry_date <= localtime.now()

    def set_attributes(self, new_attributes: dict) -> None:
        self.new_attributes = new_attributes
        self.save()
