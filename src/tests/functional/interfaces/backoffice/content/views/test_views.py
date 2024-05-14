import pytest
from django import test as django_test
from django import urls

from queenbees.core.content import models as content_models
from tests.factories import users as users_factories


@pytest.fixture
def client_with_article_permission(client: django_test.Client) -> django_test.Client:
    user = users_factories.User()
    # TODO: Add permission management
    client.force_login(user)
    return client


class TestArticleList:
    def test_view(
        self,
        client_with_article_permission: django_test.Client,
        article: content_models.Article,
    ) -> None:
        response = client_with_article_permission.get(urls.reverse("article-list"))

        assert response.status_code == 200
        assert article.name in response.content.decode()


class TestArticleDetails:
    def test_view(
        self,
        client_with_article_permission: django_test.Client,
        article: content_models.Article,
    ) -> None:
        response = client_with_article_permission.get(
            urls.reverse("article-view", kwargs={"id": article.id})
        )

        assert response.status_code == 200
        assert article.name in response.content.decode()
