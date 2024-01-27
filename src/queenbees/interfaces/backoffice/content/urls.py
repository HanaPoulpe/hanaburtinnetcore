from django import urls

from . import views

urlpatterns = [
    urls.path("articles/", views.ArticleList.as_view(), name="article-list"),
]
