from django import urls
from graphene_django import views

from queenbees.core.interfaces import urls as core_urls

urlpatterns = core_urls.urlpatterns + [
    urls.path("graphql", views.GraphQLView.as_view(graphiql=True), name="graphql"),
]
