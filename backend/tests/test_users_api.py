from http import HTTPStatus

import pytest
from faker.proxy import Faker

from pytest_lazy_fixtures import lf
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
class TestUsersApi:
    """Класс для тестов user api."""

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, None),
            (lf("user_one_client"), HTTPStatus.OK, lf("user_one")),
            (lf("superuser_client"), HTTPStatus.OK, lf("superuser")),
        ],
    )
    @pytest.mark.usefixtures("some_users")
    def test_get_users_list(self, client: APIClient, expected_status_code: int, user: User | None) -> None:
        """Проверяет получение списка пользователей различными пользователями."""
        response = client.get("/api/v1/users/")
        assert response.status_code == expected_status_code, "Код ответа отличается от ожидаемого"
        if expected_status_code == HTTPStatus.OK:
            json = response.json()
            if user.is_superuser:
                assert len(json) == User.objects.count(), "Длина ответа для суперпользователя отличается от ожидаемой"
            else:
                assert len(json) == 1, "Длина ответа отличается от ожидаемой"
                assert json[0]["id"] == str(user.id), "Идентификатор пользователя не совпадает"

    def test_create_user(self, anonymous_client: APIClient, faker: Faker) -> None:
        """Проверяет создание нового пользователя."""
        payload = {
            "username": faker.unique.user_name(),
            "email": faker.unique.email(),
            "password": faker.password(),
        }
        response = anonymous_client.post("/api/v1/users/", payload)
        json = response.json()
        user_from_db = User.objects.get(id=json["id"])
        assert response.status_code == HTTPStatus.CREATED, "Код ответа отличается от ожидаемого"
        assert User.objects.count() == 1, "Количество пользователей в базе данных отличается от ожидаемого"
        assert user_from_db is not None, "Пользователь не найден в базе данных"
        assert user_from_db.username == payload["username"], "Username пользователя не совпадает"
        assert user_from_db.email == payload["email"], "Email пользователя не совпадает"
