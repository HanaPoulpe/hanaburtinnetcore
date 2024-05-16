from typing import Self

import graphene

from queenbees.core.content import models as content_models
from queenbees.core.content import operations as content_operations
from queenbees.interfaces.api.graphql.content import _errors as errors
from queenbees.interfaces.api.graphql.content import _types as types


class CreateArticleMutation(graphene.Mutation):
    class Input:
        title = graphene.Argument(
            graphene.String,
            required=True,
            description="Article title.",
        )
        content = graphene.Argument(
            graphene.String,
            required=True,
            description="Article content.",
        )
        content_format = graphene.Argument(
            graphene.Enum.from_enum(content_models.TextFormats),
            required=True,
            description="Article content format.",
        )

    article = graphene.Field(types.ArticleType)

    def mutate(
        root,
        info: graphene.ResolveInfo,
        title: str,
        content: str,
        content_format: content_models.TextFormats,
    ) -> Self:
        if content_models.Article.objects.filter(name=title).exists():
            return errors.ARTICLE_ALREADY_EXISTS()

        article = content_operations.create_article(
            name=title,
            content=content,
            content_format=content_format,
            user=info.context.user,
        )

        return CreateArticleMutation(article=article)
