import graphene


class ErrorType(graphene.ObjectType):
    code = graphene.String(description="Error code.")
    description = graphene.String(description="Error description.")
