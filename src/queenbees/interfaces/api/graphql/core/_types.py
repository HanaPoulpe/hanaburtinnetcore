import graphene
import graphene_django
from django.contrib.auth import models as auth_models


class ErrorType(graphene.ObjectType):
    code = graphene.String(description="Error code.")
    description = graphene.String(description="Error description.")


class UserType(graphene_django.DjangoObjectType):
    class Meta:
        model = auth_models.User
        fields = ("username",)
