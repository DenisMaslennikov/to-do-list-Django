from typing import Type

import pytest
from django.contrib.auth import get_user_model
from django.db.models import Model
from faker import Faker
from faker.generator import random
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token

from classifiers.models import TaskStatus
from tasks.models import Task
from tests.constants import COMPLETED_TASK_STATUS_ID
from users.models import User


@pytest.fixture
def user_model() -> Type[User]:
    """Фикстура модели пользователя."""
    return get_user_model()


@pytest.fixture
def faker() -> Faker:
    """Фикстура фейкера."""
    return Faker("ru_RU")


@pytest.fixture
def user_one(user_model: Type[User], faker: Faker) -> User:
    """Фикстура первого пользователя."""
    password = faker.password()
    return user_model.objects.create_user(
        email=faker.unique.email(),
        username=faker.unique.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        middle_name=faker.middle_name(),
        password=password,
    )


@pytest.fixture
def user_two(user_model: Type[User], faker: Faker) -> User:
    """Фикстура второго пользователя."""
    password = faker.password()
    return user_model.objects.create_user(
        email=faker.unique.email(),
        username=faker.unique.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        middle_name=faker.middle_name(),
        password=password,
    )


@pytest.fixture
def user_one_password(user_one: User, faker: Faker) -> str:
    """Пароль первого пользователя."""
    password = faker.password()
    user_one.set_password(password)
    user_one.save()
    return password


@pytest.fixture
def user_two_password(user_two: User, faker: Faker) -> str:
    """Пароль второго пользователя."""
    password = faker.password()
    user_two.set_password(password)
    user_two.save()
    return password


@pytest.fixture
def superuser_password(superuser: User, faker: Faker) -> str:
    """Пароль суперпользователя."""
    password = faker.password()
    superuser.set_password(password)
    superuser.save()
    return password


@pytest.fixture
def superuser(user_model: Type[User], faker: Faker) -> User:
    """Фикстура суперпользователя."""
    password = faker.password()
    return user_model.objects.create_superuser(
        email=faker.unique.email(),
        username=faker.unique.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        middle_name=faker.middle_name(),
        password=password,
    )


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
def superuser_access_token(superuser: User) -> Token:
    """Access токен суперпользователя."""
    return AccessToken.for_user(superuser)


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


@pytest.fixture
def superuser_client(superuser_access_token) -> APIClient:
    """Клиент суперпользователя."""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {superuser_access_token}")
    return client


@pytest.fixture
def users(user_model: Type[User], faker: Faker) -> list[User]:
    """Создает несколько пользователей."""
    users = [
        user_model.objects.create_user(
            email=faker.unique.email(),
            username=faker.unique.user_name(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            middle_name=faker.middle_name(),
            password=faker.password(),
        )
        for _ in range(faker.random_int(5, 25))
    ]
    return users


@pytest.fixture
def user_one_tasks(user_one: User, faker: Faker) -> list[Task]:
    """Создает несколько задач."""
    tasks_status: list[TaskStatus] = TaskStatus.objects.all()

    tasks = []
    for _ in range(faker.random_int(5, 25)):
        completed_at = None
        complete_before = None
        if faker.random_int(1, 100) < 50:
            complete_before = faker.date_time()
        task_status = random.choice(tasks_status)
        if task_status.id == COMPLETED_TASK_STATUS_ID:
            completed_at = faker.date_time()

        task = Task(
            title=faker.text(max_nb_chars=100),
            description=faker.text(max_nb_chars=500),
            task_status=task_status,
            user=user_one,
            completed_at=completed_at,
            complete_before=complete_before,
        )
        tasks.append(task)

    Task.objects.bulk_create(tasks)
    return tasks
