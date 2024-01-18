import pytest
from django.contrib.auth import models as auth_models
from faker import Faker

from tests.factories import users as users_factories

faker = Faker()


@pytest.fixture
def user_with_password() -> tuple[auth_models.User, str]:
    user: auth_models.User = users_factories.User()
    password = faker.password()
    user.set_password(password)
    user.save()

    return user, password
