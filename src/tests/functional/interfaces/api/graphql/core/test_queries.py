import pytest

from queenbees.interfaces.api.graphql import errors
from tests.types import GraphQLClient


class TestErrorQuery:
    MY_ERROR = errors.GraphQLError(
        perimeter="TESTS",
        name="MY_ERROR",
        description="Random test exception.",
    )

    def test_all_graphql_exceptions(self, graphql_client: GraphQLClient) -> None:
        query = """
        query {
            allErrors {
                code
                description
            }
        }
        """

        response = graphql_client.query(query)

        response.assert_no_errors()
        all_errors = response.data["allErrors"]
        assert {
            "code": self.MY_ERROR.code,
            "description": self.MY_ERROR.description,
        } in all_errors

    @pytest.mark.parametrize(
        "perimeter,expected_errors",
        (
            (
                "TESTS",
                [
                    {
                        "code": MY_ERROR.code,
                        "description": MY_ERROR.description,
                    }
                ],
            ),
            ("TEST_NONE", []),
        ),
        ids=("TESTS", "TEST_NONE"),
    )
    def test_all_graphql_exception_for_perimeter(
        self, graphql_client: GraphQLClient, perimeter: str, expected_errors: list[dict]
    ) -> None:
        query = f"""
        query {{
            allErrors(perimeter: "{perimeter}") {{
                code
                description
            }}
        }}
        """

        response = graphql_client.query(query)

        response.assert_no_errors()
        assert response.data["allErrors"] == expected_errors
