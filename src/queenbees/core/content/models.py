import uuid

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import models

from queenbees.utils import localtime


# Enums #
class TextFormats(models.TextChoices):
    PLAIN_TEXT = "PLAIN", "Plain Text"
    HTML = "HTML", "HTML"
    MARKDOWN = "MD", "Markdown"


class FileSourceTypes(models.TextChoices):
    EXTERNAL = "EXTERNAL", "File stored on an external storage"


# Models #
class GenericContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        blank=False,
        null=False,
    )

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
