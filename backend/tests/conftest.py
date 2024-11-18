from typing import Type

import pytest
from django.contrib.auth import get_user_model
from django.db.models import Model
from faker import Faker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token

from tasks.models import User


@pytest.fixture
def user_model() -> Type[Model]:
    """Фикстура модели пользователя."""
    return get_user_model()


@pytest.fixture
def faker() -> Faker:
    """Фикстура фейкера."""
    return Faker("ru_RU")


@pytest.fixture
def user_one(user_model: Type[Model], faker: Faker) -> User:
    """Фикстура первого пользователя."""
    return user_model(
        email=faker.unique.email(),
        username=faker.unique.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        middle_name=faker.middle_name(),
    )


@pytest.fixture
def user_two(user_model: Type[Model], faker: Faker) -> User:
    """Фикстура второго пользователя."""
    return user_model(
        email=faker.unique.email(),
        username=faker.unique.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        middle_name=faker.middle_name(),
    )


@pytest.fixture
def user_one_password(user_one: User, faker: Faker) -> str:
    """Пароль первого пользователя."""
    password = faker.password()
    user_one.set_password(password)
    user_one.save()
    return password


@pytest.fixture
def user_one_access_token(user_one: User) -> Token:
    """Access токен первого пользователя."""
    return AccessToken.for_user(user_one)


@pytest.fixture
def user_one_refresh_token(user_one: User) -> Token:
    """Рефрреш токен первого пользователя."""
    return RefreshToken.for_user(user_one)


@pytest.fixture
def user_two_access_token(user_two: User) -> Token:
    """Access токен второго пользователя."""
    return AccessToken.for_user(user_two)


@pytest.fixture
def anonymous_client() -> APIClient:
    """Неавторизованый клиент."""
    return APIClient()


@pytest.fixture
def user_one_client(user_one_access_token) -> APIClient:
    """Клиент первого пользователя."""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_one_access_token}")
    return client


@pytest.fixture
def user_two_client(user_two_access_token) -> APIClient:
    """Клиент второго пользователя."""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_two_access_token}")
    return client
