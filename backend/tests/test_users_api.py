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
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "middle_name": faker.middle_name(),
        }
        response = anonymous_client.post("/api/v1/users/", payload)
        json = response.json()
        user_from_db = User.objects.get(id=json["id"])
        assert response.status_code == HTTPStatus.CREATED, "Код ответа отличается от ожидаемого"
        assert User.objects.count() == 1, "Количество пользователей в базе данных отличается от ожидаемого"
        assert user_from_db is not None, "Пользователь не найден в базе данных"
        assert user_from_db.username == payload["username"], "Username пользователя не совпадает"
        assert user_from_db.email == payload["email"], "Email пользователя не совпадает"
        assert user_from_db.first_name == payload["first_name"], "Имя пользователя не совпадает"
        assert user_from_db.last_name == payload["last_name"], "Фамилия пользователя не совпадает"
        assert user_from_db.middle_name == payload["middle_name"], "Отчество пользователя не совпадает"

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, lf("user_one")),
            (lf("user_one_client"), HTTPStatus.OK, lf("user_one")),
            (lf("superuser_client"), HTTPStatus.OK, lf("superuser")),
        ],
    )
    def test_get_user_by_id_self_id(self, client: APIClient, expected_status_code: int, user: User) -> None:
        """Проверяет получение пользователем по id самого себя."""
        response = client.get(f"/api/v1/users/{user.id}/")

        assert response.status_code == expected_status_code, "Код ответа отличается от ожидаемого"
        if expected_status_code == HTTPStatus.OK:
            json = response.json()
            assert json["id"] == str(user.id), "Идентификатор пользователя не совпадает"
            assert json["username"] == user.username, "Username пользователя не совпадает"
            assert json["email"] == user.email, "Email пользователя не совпадает"
            assert json["first_name"] == user.first_name, "Имя пользователя не совпадает"
            assert json["last_name"] == user.last_name, "Фамилия пользователя не совпадает"
            assert json["middle_name"] == user.middle_name, "Отчество пользователя не совпадает"

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, lf("user_one")),
            (lf("user_one_client"), HTTPStatus.NOT_FOUND, lf("user_two")),
            (lf("superuser_client"), HTTPStatus.OK, lf("user_one")),
        ],
    )
    def test_get_user_by_id_another_user_id(self, client: APIClient, expected_status_code: int, user: User) -> None:
        """Проверяет получение пользователем по id самого себя."""
        response = client.get(f"/api/v1/users/{user.id}/")

        assert response.status_code == expected_status_code, "Код ответа отличается от ожидаемого"
        if expected_status_code == HTTPStatus.OK:
            json = response.json()
            assert json["id"] == str(user.id), "Идентификатор пользователя не совпадает"
            assert json["username"] == user.username, "Username пользователя не совпадает"
            assert json["email"] == user.email, "Email пользователя не совпадает"
            assert json["first_name"] == user.first_name, "Имя пользователя не совпадает"
            assert json["last_name"] == user.last_name, "Фамилия пользователя не совпадает"
            assert json["middle_name"] == user.middle_name, "Отчество пользователя не совпадает"
