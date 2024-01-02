from typing import Any

import factory
import lorem
from factory.django import DjangoModelFactory

from queenbees.core.content import models


def lazy_sentence(*args: Any) -> str:
    return lorem.get_sentence()[:100]


def lazy_paragraph(*args: Any) -> str:
    return lorem.get_paragraph()


class Article(DjangoModelFactory):
    class Meta:
        model = models.Article

    name = factory.LazyAttribute(lazy_sentence)
    format = models.TextFormats.PLAIN_TEXT.value
    content = factory.LazyAttribute(lazy_paragraph)


class File(DjangoModelFactory):
    class Meta:
        model = models.File

    name = factory.LazyAttribute(lazy_sentence)
    internal_location = None
    external_location = None
