from django import http
from django.db import models
from django.views import generic

from queenbees.core.content import models as content_models


class ArticleList(generic.ListView):
    model = content_models.Article
    template_name = "content/article-list.html"


class ArticleView(generic.DetailView):
    model = content_models.Article
    template_name = "content/article-detail.html"

    def get_object(
        self, queryset: models.QuerySet[content_models.Article] | None = None
    ) -> content_models.Article:
        if queryset is None:
            queryset = self.model.objects

        try:
            article = queryset.get(id=self.kwargs["id"])
            return article
        except content_models.Article.DoesNotExist:
            raise http.Http404()
