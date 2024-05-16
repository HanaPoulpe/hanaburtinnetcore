__all__ = ["Query", "TYPES"]

from . import _queries as queries
from . import _types as types


class Query(queries.ErrorQuery):
    pass


TYPES = [types.ErrorType, types.UserType]
