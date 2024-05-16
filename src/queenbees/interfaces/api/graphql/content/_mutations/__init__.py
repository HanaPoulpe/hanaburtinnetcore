__all__ = ["Mutation"]

import graphene

from . import article_drafts, articles


class Mutation(graphene.ObjectType):
    save_article_draft = article_drafts.SaveArticleDraftMutation.Field()
    commit_article_draft = article_drafts.CommitArticleDraftMutation.Field()

    create_article = articles.CreateArticleMutation.Field()
