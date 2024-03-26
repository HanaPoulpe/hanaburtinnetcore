import uuid

from django.db import models

from queenbees.utils import localtime


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
    )
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)

    class Meta:
        abstract = True


class UUIDIdentifierMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    class Meta:
        abstract = True
