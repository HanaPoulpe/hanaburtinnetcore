from queenbees.core.content import models as content_models


def get_article_by_name(name: str) -> content_models.Article:
    """
    Return the article matching the given name.

    :param name: Article name
    :return: Article object
    :raise content_models.Article.DoesNotExist: Article not found
    """
    return content_models.Article.objects.get(name=name)
