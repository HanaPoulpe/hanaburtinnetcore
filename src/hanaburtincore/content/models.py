import uuid

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import models


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


class Article(GenericContent):
    format = models.CharField(max_length=30, choices=TextFormats.choices, null=False, blank=False)
    content = models.TextField()


class File(GenericContent):
    source_type = models.CharField(
        max_length=30, choices=FileSourceTypes.choices, null=False, blank=False
    )
    internal_location = models.CharField(max_length=300, null=True, blank=False)
    external_location = models.CharField(max_length=300, null=True, blank=False)

    @property
    def public_url(self) -> str:
        return self.external_location or settings.BROKEN_MEDIA_URL  # type: ignore
