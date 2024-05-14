import attr
import pytest
from django import test as django_test
from django import urls
from django.contrib.auth import models as auth_models
from faker import Faker

from tests.factories import users as users_factories

faker = Faker()


@attr.define
class RejectedLogin:
    username: str
    password: str


class TestPasswordLogin:
    @pytest.fixture
    def rejected_logins(self, request: pytest.FixtureRequest) -> RejectedLogin:
        if request.param == "invalid_password":
            user = users_factories.User()
            user_password = faker.password()
            user.set_password(user_password)

            while True:
                wrong_password = faker.password()
                if wrong_password != user_password:
                    return RejectedLogin(
                        user.username,
                        wrong_password,
                    )

        if request.param == "password_login_not_allowed":
            user = users_factories.User()
            user.set_unusable_password()
            return RejectedLogin(
                user.username,
                faker.password(),
            )

        if request.param == "invalid_user":
            return RejectedLogin(
                faker.user_name(),
                faker.password(),
            )

        raise Exception(f"Invalid test parameter: {request.param}")

    def test_login_successful(
        self, client: django_test.Client, user_with_password: tuple[auth_models.User, str]
    ) -> None:
        user, password = user_with_password

        assert client.login(username=user, password=password)

    @pytest.mark.parametrize(
        "rejected_logins",
        ["invalid_password", "password_login_not_allowed", "invalid_user"],
        indirect=True,
    )
    def test_login_failed(
        self, client: django_test.Client, rejected_logins: RejectedLogin
    ) -> None:
        assert not client.login(
            username=rejected_logins.username, password=rejected_logins.password
        )

    def test_login_page(self, client: django_test.Client) -> None:
        response = client.get(urls.reverse("login"))
        assert response.status_code == 200
