__all__ = ["Query", "Mutations", "TYPES"]

import graphene

from . import _mutations, _queries, _types


class Query(_queries.ArticleQuery, _queries.ArticleDraftQuery):
    pass


class Mutations(_mutations.Mutation):
    pass


TYPES = [
    _types.ArticleType,
    _types.ArticleDraftType,
    _types.FileType,
]
