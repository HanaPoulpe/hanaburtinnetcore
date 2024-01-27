from django.views import generic

from queenbees.core.content import models as content_models


class ArticleList(generic.ListView):
    model = content_models.Article
    template_name = "content/article-list.html"
