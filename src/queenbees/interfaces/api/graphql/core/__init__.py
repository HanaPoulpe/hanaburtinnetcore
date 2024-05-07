__all__ = ["Query", "TYPES"]

import graphene

from . import _queries as queries
from . import _types as types


class Query(queries.ErrorQuery):
    pass


TYPES = [types.ErrorType]
