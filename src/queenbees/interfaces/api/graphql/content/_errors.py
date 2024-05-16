from queenbees.interfaces.api.graphql import errors

ARTICLE_NOT_FOUND = errors.GraphQLError(
    name="ARTICLE_NOT_FOUND",
    description="Article not found.",
    perimeter="CONTENT",
)
ARTICLE_ALREADY_EXISTS = errors.GraphQLError(
    name="ARTICLE_ALREADY_EXISTS",
    description="Article with same title already exists.",
    perimeter="CONTENT",
)
DRAFT_NOT_FOUND = errors.GraphQLError(
    name="DRAFT_NOT_FOUND",
    description="Draft not found.",
    perimeter="CONTENT",
)
