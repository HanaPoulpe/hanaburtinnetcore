__all__ = ["schema"]

import graphene

from . import content, core


class Query(content.Query, core.Query):
    pass


class Mutations(content.Mutations):
    pass


TYPES = content.TYPES + core.TYPES

schema = graphene.Schema(query=Query, mutation=Mutations, types=TYPES)
