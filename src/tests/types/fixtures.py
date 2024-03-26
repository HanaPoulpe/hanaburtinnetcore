import attr

from queenbees.core.content import models as content_models


@attr.frozen
class ArticleDraftFixture:
    article: content_models.Article
    draft: content_models.ArticleDraft
