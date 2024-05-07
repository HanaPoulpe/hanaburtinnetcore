import graphene

from queenbees.interfaces.api.graphql import errors

from . import _types as types


class ErrorQuery(graphene.ObjectType):
    all_errors = graphene.List(
        types.ErrorType,
        description="Retrieve all errors for a specific perimeter.",
        perimeter=graphene.String(
            description="Perimeter of the error.",
            required=False,
        ),
    )

    def resolve_all_errors(
        root, info: graphene.ResolveInfo, perimeter: str | None = None
    ) -> list[types.ErrorType]:
        all_errors = [error for error, _ in errors.graphql_errors]

        if perimeter:
            all_errors = [error for error in all_errors if error.perimeter == perimeter]

        return all_errors
