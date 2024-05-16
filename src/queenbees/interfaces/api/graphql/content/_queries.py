import uuid

import graphene

from queenbees.core.content import models as content_models

from . import _errors as errors
from . import _types as types


class ArticleQuery(graphene.ObjectType):
    all_articles = graphene.List(types.ArticleType, description="All articles")
    published_articles = graphene.List(
        types.ArticleType,
        description="Published articles",
    )
    article_by_title = graphene.Field(
        types.ArticleType,
        title=graphene.String(required=True, description="Name of the article"),
        description="Get an article by its name.",
    )
    article_by_id = graphene.Field(
        types.ArticleType,
        id=graphene.UUID(required=True, description="ID of the article"),
        description="Get an article by its ID.",
    )
    articles_by_author = graphene.List(
        types.ArticleType,
        author=graphene.String(required=True, description="ID of the author"),
        description="Get all articles by an author.",
    )

    def resolve_all_articles(root, info: graphene.ResolveInfo) -> list[types.ArticleType]:
        return content_models.Article.objects.all()

    def resolve_published_articles(root, info: graphene.ResolveInfo) -> list[types.ArticleType]:
        return content_models.Article.objects.published()

    def resolve_article_by_title(
        root, info: graphene.ResolveInfo, title: str
    ) -> types.ArticleType:
        try:
            return content_models.Article.objects.get(name=title)
        except content_models.Article.DoesNotExist:
            return errors.ARTICLE_NOT_FOUND()

    def resolve_article_by_id(
        root, info: graphene.ResolveInfo, id: uuid.UUID
    ) -> types.ArticleType:
        try:
            return content_models.Article.objects.get(id=id)
        except content_models.Article.DoesNotExist:
            return errors.ARTICLE_NOT_FOUND()

    def resolve_articles_by_author(
        root,
        info: graphene.ResolveInfo,
        author: str,
    ) -> list[types.ArticleType]:
        return content_models.Article.objects.filter(created_by__username=author)


class ArticleDraftQuery(graphene.ObjectType):
    latest_draft_for_article = graphene.Field(
        types.ArticleDraftType,
        article_id=graphene.UUID(required=True, description="ID of the article"),
        author=graphene.String(required=False, description="ID of the author"),
        description="Get the latest draft for an article.",
    )

    def resolve_latest_draft_for_article(
        root,
        info: graphene.ResolveInfo,
        article_id: uuid.UUID,
        author: str | None = None,
    ) -> types.ArticleDraftType:
        drafts = content_models.ArticleDraft.objects.filter(article_id=article_id)

        if author:
            drafts = drafts.filter(working_user__username=author)

        if drafts.count() == 0:
            return errors.DRAFT_NOT_FOUND()

        return drafts.latest("updated_at")
