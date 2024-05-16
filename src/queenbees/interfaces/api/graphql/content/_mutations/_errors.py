from queenbees.interfaces.api.graphql import errors

NO_CHANGES_ERROR = errors.GraphQLError(
    name="NO_CHANGES",
    description="No changes to save.",
    perimeter="CONTENT",
)
ARTICLE_NAME_ALREADY_USED = errors.GraphQLError(
    name="ARTICLE_NAME_ALREADY_USED",
    description="Article name already in use.",
    perimeter="CONTENT",
)
INVALID_PARAMETERS = errors.GraphQLError(
    name="INVALID_PARAMETERS",
    description="Invalid parameters.",
    perimeter="CONTENT",
)
