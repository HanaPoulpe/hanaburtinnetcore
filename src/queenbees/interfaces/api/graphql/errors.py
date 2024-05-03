from typing import Any

import attrs
import graphql
from django.conf import settings

from queenbees.utils import localtime, registry


@attrs.frozen(slots=True, kw_only=True)
class GraphQLError:
    perimeter: str
    name: str
    description: str
    _number: int = attrs.field(init=False)

    @_number.default
    def _number_default(self) -> int:
        return len(graphql_errors)

    def __attrs_post_init__(self) -> None:
        graphql_errors.register((self.perimeter, self.name), self)

    @property
    def code(self) -> str:
        return f"GQ-{self.perimeter}-{self._number:04X}-{self.name}"

    def __call__(
        self,
        message: str | None = None,
        exception: Exception | None = None,
        details: dict[str, Any] | None = None,
    ) -> graphql.GraphQLError:
        extensions = {
            "code": self.code,
            "timestamp": localtime.now().isoformat(),
        }

        if details:
            extensions["detials"] = details

        return graphql.GraphQLError(
            message=message or self.description,
            extensions=extensions,
            original_error=exception if settings.GRAPHENE_SHOW_ERRORS else None,
        )


graphql_errors: registry.Registry[tuple[str, str], GraphQLError] = registry.Registry()
