from typing import Self

import graphene
import graphene_django

from queenbees.core.content import models as content_models


class ArticleType(graphene_django.DjangoObjectType):
    class Meta:
        model = content_models.Article
        fields = ("id", "name", "format", "content", "published_at", "redacted_at")

    status = graphene.String()

    def resolve_status(self, info: graphene.ResolveInfo) -> content_models.Article.Status:
        return self.status


class FileType(graphene_django.DjangoObjectType):
    class Meta:
        model = content_models.File
        fields = ("id", "name", "public_url")


class ArticleDraftType(graphene_django.DjangoObjectType):
    class Meta:
        model = content_models.ArticleDraft
        fields = ("id", "article", "working_user", "new_attributes")
