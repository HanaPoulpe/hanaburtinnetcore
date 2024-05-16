from typing import Any

import factory
import lorem
from factory.django import DjangoModelFactory

from queenbees.core.content import models
from tests.factories import users as users_factory


def lazy_sentence(*args: Any) -> str:
    return lorem.get_sentence()[:100]


def lazy_paragraph(*args: Any) -> str:
    return lorem.get_paragraph()


def lasy_draft(*args: Any) -> dict[str, str | models.TextFormats | None]:
    return {
        "name": lorem.get_sentence()[:100],
        "format": models.TextFormats.PLAIN_TEXT.value,
        "content": lorem.get_paragraph(),
    }


class Article(DjangoModelFactory):
    class Meta:
        model = models.Article

    name = factory.LazyAttribute(lazy_sentence)
    format = models.TextFormats.PLAIN_TEXT.value
    content = factory.LazyAttribute(lazy_paragraph)
    created_by = factory.SubFactory(users_factory.User)


class File(DjangoModelFactory):
    class Meta:
        model = models.File

    name = factory.LazyAttribute(lazy_sentence)
    internal_location = None
    external_location = None


class ArticleDraft(DjangoModelFactory):
    class Meta:
        model = models.ArticleDraft

    new_attributes = factory.LazyAttribute(lasy_draft)
    working_user = factory.SubFactory(users_factory.User)
    article = factory.SubFactory(Article)
