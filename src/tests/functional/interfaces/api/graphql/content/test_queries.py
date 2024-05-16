import uuid

import pytest
import time_machine

from queenbees.core.content import models as content_models
from queenbees.interfaces.api.graphql.content import _errors as content_errors
from tests.types import ArticleDraftFixture, GraphQLClient, GraphQLResponse


class TestArticleQueries:
    @pytest.fixture(autouse=True)
    def set_time(
        self, time_machine: time_machine.TimeMachineFixture
    ) -> time_machine.TimeMachineFixture:
        time_machine.move_to("2024-05-16", False)
        return time_machine

    def assert_article_in_response(
        self,
        response: list[dict],
        article: content_models.Article,
        msg: str = "",
    ) -> None:
        assert {
            "id": article.id,
            "name": article.name,
            "publishedAt": article.published_at,
            "redactedAt": article.redacted_at,
            "status": article.status,
        } in response, msg

    def assert_response_matches_article_list(
        self,
        response: list[dict],
        article_list: list[content_models.Article],
        msg: str = "",
    ) -> None:
        for i, article in enumerate(article_list):
            try:
                serialized_article = {
                    "id": str(article.id),
                    "name": article.name,
                    "publishedAt": article.published_at and article.published_at.isoformat(),
                    "redactedAt": article.redacted_at and article.redacted_at.isoformat(),
                    "status": article.status.value,
                }
                j = response.index(serialized_article)
                response.pop(j)
            except ValueError:
                breakpoint()
                assert False, msg or f"{article} not in response"

        assert not response, msg or f"{response} not in articles"

    @pytest.mark.parametrize(
        "many_articles,many_published_articles,many_redacted_articles",
        ((2, 2, 2),),
        indirect=["many_articles", "many_published_articles", "many_redacted_articles"],
        ids=("",),
    )
    def test_all_articles(
        self,
        many_articles: list[content_models.Article],
        many_published_articles: list[content_models.Article],
        many_redacted_articles: list[content_models.Article],
        graphql_client: GraphQLClient,
    ) -> None:
        query = """
        query {
            allArticles {
                id
                name
                publishedAt
                redactedAt
                status
            }
        }
        """

        response = graphql_client.query(query)

        response.assert_no_errors()
        self.assert_response_matches_article_list(
            response.data["allArticles"],
            [*many_articles, *many_published_articles, *many_redacted_articles],
        )

    @pytest.mark.parametrize(
        "many_articles,many_published_articles,many_redacted_articles",
        ((2, 2, 2),),
        indirect=["many_articles", "many_published_articles", "many_redacted_articles"],
        ids=("",),
    )
    def test_published_articles(
        self,
        many_articles: list[content_models.Article],
        many_published_articles: list[content_models.Article],
        many_redacted_articles: list[content_models.Article],
        graphql_client: GraphQLClient,
    ) -> None:
        query = """
        query {
            publishedArticles {
                id
                name
                publishedAt
                redactedAt
                status
            }
        }
        """

        response = graphql_client.query(query)

        response.assert_no_errors()
        self.assert_response_matches_article_list(
            response.data["publishedArticles"],
            many_published_articles,
        )

    def test_article_by_name(
        self,
        article: content_models.Article,
        graphql_client: GraphQLClient,
    ) -> None:
        query = f"""
        query {{
            articleByTitle(title: "{article.name}") {{
                id
                name
                publishedAt
                redactedAt
                status
            }}
        }}
        """

        response = graphql_client.query(query)

        response.assert_no_errors()

        returned_article = response.data["articleByTitle"]
        assert returned_article["id"] == str(article.id)
        assert returned_article["name"] == article.name
        assert returned_article["publishedAt"] is None
        assert returned_article["redactedAt"] is None
        assert returned_article["status"] == article.status.value

    def test_article_by_name_not_found(
        self,
        article: content_models.Article,
        graphql_client: GraphQLClient,
    ) -> None:
        query = """
        query {
            articleByTitle(title: "!!NoMatch!!") {
                id
                name
                publishedAt
                redactedAt
                status
            }
        }
        """

        response = graphql_client.query(query)

        assert response.errors
        error = response.errors[0]
        assert error["extensions"]["code"] == content_errors.ARTICLE_NOT_FOUND.code

    def test_article_by_id(
        self,
        article: content_models.Article,
        graphql_client: GraphQLClient,
    ) -> None:
        query = f"""
        query {{
            articleById(id: "{article.id!s}") {{
                id
                name
                publishedAt
                redactedAt
                status
            }}
        }}
        """

        response = graphql_client.query(query)

        response.assert_no_errors()

        returned_article = response.data["articleById"]
        assert returned_article["id"] == str(article.id)
        assert returned_article["name"] == article.name
        assert returned_article["publishedAt"] is None
        assert returned_article["redactedAt"] is None
        assert returned_article["status"] == article.status.value

    def test_article_by_id_not_found(
        self,
        article: content_models.Article,
        graphql_client: GraphQLClient,
    ) -> None:
        query = f"""
        query {{
            articleById(id: "{uuid.uuid4()!s}") {{
                id
                name
                publishedAt
                redactedAt
                status
            }}
        }}
        """

        response = graphql_client.query(query)

        assert response.errors
        error = response.errors[0]
        assert error["extensions"]["code"] == content_errors.ARTICLE_NOT_FOUND.code

    def test_articles_by_author(
        self,
        article: content_models.Article,
        graphql_client: GraphQLClient,
    ) -> None:
        author = article.created_by
        assert author

        query = f"""
        query {{
            articlesByAuthor(author: "{author.username!s}") {{
                id
                name
                publishedAt
                redactedAt
                status
            }}
        }}
        """

        response = graphql_client.query(query)

        response.assert_no_errors()
        self.assert_response_matches_article_list(
            response.data["articlesByAuthor"],
            [article],
        )


class TestArticleDraftQueries:
    @pytest.fixture(autouse=True)
    def set_time(
        self, time_machine: time_machine.TimeMachineFixture
    ) -> time_machine.TimeMachineFixture:
        time_machine.move_to("2024-05-16", False)
        return time_machine

    def test_latest_draft_for_article(
        self,
        article_draft: ArticleDraftFixture,
        graphql_client: GraphQLClient,
    ) -> None:
        query = f"""
        query {{
            latestDraftForArticle(articleId: "{article_draft.article.id}") {{
                id
                article {{
                    id
                }}
                workingUser {{
                    username
                }}
                newAttributes
            }}
        }}
        """

        response = graphql_client.query(query)

        response.assert_no_errors()
        data = response.data["latestDraftForArticle"]
        assert data["id"] == str(article_draft.draft.id)
        assert data["article"]["id"] == str(article_draft.article.id)
        assert data["workingUser"]["username"] == str(article_draft.draft.working_user.username)

    def test_latest_draft_for_article_with_username(
        self,
        article_draft: ArticleDraftFixture,
        graphql_client: GraphQLClient,
    ) -> None:
        query = f"""
        query {{
            latestDraftForArticle(
                articleId: "{article_draft.article.id}", 
                author: "{article_draft.draft.working_user.username}"
            ) {{
                id
                article {{
                    id
                }}
                workingUser {{
                    username
                }}
                newAttributes
            }}
        }}
        """

        response = graphql_client.query(query)

        response.assert_no_errors()
        data = response.data["latestDraftForArticle"]
        assert data["id"] == str(article_draft.draft.id)
        assert data["article"]["id"] == str(article_draft.article.id)
        assert data["workingUser"]["username"] == str(article_draft.draft.working_user.username)

    def test_latest_draft_for_article_not_found(
        self,
        article: content_models.Article,
        graphql_client: GraphQLClient,
    ) -> None:
        query = f"""
        query {{
            latestDraftForArticle(articleId: "{article.id}") {{
                id
                article {{
                    id
                }}
                workingUser {{
                    username
                }}
                newAttributes
            }}
        }}
        """

        response = graphql_client.query(query)

        assert response.errors
        error = response.errors[0]
        assert error["extensions"]["code"] == content_errors.DRAFT_NOT_FOUND.code
