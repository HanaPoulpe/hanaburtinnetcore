import json
from typing import Any, Protocol, cast

import pytest
from django import http, urls
from django.test import client


class HttpJSonResponse(http.HttpResponse):
    def json(self) -> dict[str, Any]:
        raise NotImplementedError()


class GraphQLResponse:
    def __init__(self, response: http.HttpResponse) -> None:
        self.http_response: HttpJSonResponse = cast(HttpJSonResponse, response)

    @property
    def json(self) -> dict[str, Any]:
        return self.http_response.json()

    @property
    def data(self) -> dict[str, Any]:
        return self.json.get("data", {})

    @property
    def errors(self) -> list[dict[str, Any]]:
        return self.json.get("errors", [])

    def assert_no_errors(self, msg: str = "") -> None:
        assert not self.errors, msg or self.errors

    def assert_ok_status(self, msg: str) -> None:
        assert self.http_response.status_code == 200, msg or self.errors


class GraphQLClient(client.Client):
    def __init__(self) -> None:
        self.graphql_url = urls.reverse("graphql")
        super().__init__()

    def query(
        self,
        query: str,
        operation_name: str | None = None,
        variables: dict | None = None,
    ) -> GraphQLResponse:
        data = {
            "query": query,
            "variables": variables or {},
        }

        if operation_name:
            data["operationName"] = operation_name

        response = self.post(
            path=self.graphql_url,
            data=json.dumps(data),
            content_type="application/json",
        )
        return GraphQLResponse(response)  # type: ignore


@pytest.fixture
def graphql_client() -> GraphQLClient:
    return GraphQLClient()
