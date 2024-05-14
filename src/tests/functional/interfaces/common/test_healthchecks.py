import pytest
from django import test as django_test
from django import urls


class TestHealthChecks:
    def test_health_check(self, client: django_test.Client) -> None:
        response = client.get(urls.reverse("health_check:health_check_home"))

        assert response.status_code == 200
