from typing import Self

import graphene

from queenbees.core.content import models as content_models
from queenbees.core.content import operations as content_operations
from queenbees.interfaces.api.graphql.content import _errors as content_errors
from queenbees.interfaces.api.graphql.content import _types as types

from . import _errors as errors


class SaveArticleDraftMutation(graphene.Mutation):
    class Input:
        article_id = graphene.Argument(
            graphene.ID,
            description="ID of the article.",
            required=True,
        )
        title = graphene.Argument(
            graphene.String,
            required=False,
            description="New article title.",
        )
        content = graphene.Argument(
            graphene.String,
            required=False,
            description="New article content.",
        )
        content_format = graphene.Argument(
            graphene.Enum.from_enum(content_models.TextFormats),
            required=False,
            description="New article content format.",
        )

    draft = graphene.Field(types.ArticleDraftType)

    def mutate(
        root,
        info: graphene.ResolveInfo,
        article_id: str,
        title: str | None,
        content: str | None,
        content_format: content_models.TextFormats | None,
    ) -> Self:
        if (article_id, title, content, content_format) == (None, None, None, None):
            return errors.NO_CHANGES_ERROR()

        try:
            article = content_models.Article.objects.get(id=article_id)
        except content_models.Article.DoesNotExist:
            return content_errors.ARTICLE_NOT_FOUND()

        draft = content_operations.get_or_create_article_draft(
            content=article,
            user=info.context.user,
        )

        draft.new_attributes = {
            "name": title,
            "content": content,
            "content_format": content_format,
        }

        try:
            draft.save()
        except content_models.ArticleDraft.ArticleNameAlreadyUsedException as err:
            return errors.ARTICLE_NAME_ALREADY_USED(
                exception=err,
            )

        return SaveArticleDraftMutation(draft=draft)


class CommitArticleDraftMutation(graphene.Mutation):
    class Input:
        draft_id = graphene.Argument(
            graphene.ID,
            required=True,
            description="ID of the draft to commit.",
        )

    article = graphene.Field(types.ArticleType)

    def mutate(
        root,
        info: graphene.ResolveInfo,
        draft_id: str,
    ) -> Self:
        try:
            draft = content_models.ArticleDraft.objects.get(id=draft_id)
        except content_models.ArticleDraft.DoesNotExist:
            return content_errors.DRAFT_NOT_FOUND()

        try:
            article = content_operations.update_article(
                user=info.context.user,
                article=draft.article,
                draft=draft,
            )
        except content_operations.DuplicateArticleError:
            return errors.ARTICLE_NAME_ALREADY_USED()
        except content_operations.InvalidParametersError as err:
            return errors.INVALID_PARAMETERS(
                message=err.message,
                exception=err,
            )

        return CommitArticleDraftMutation(article=article)
