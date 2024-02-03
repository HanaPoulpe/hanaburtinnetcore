from django import urls

from . import views

urlpatterns = [
    urls.path("articles/", views.ArticleList.as_view(), name="article-list"),
    urls.path("article/<uuid:id>/", views.ArticleView.as_view(), name="article-view"),
]
