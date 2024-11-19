from http import HTTPStatus
import random
from tkinter.constants import NORMAL

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
            (lf("user_one_client"), HTTPStatus.NOT_FOUND, lf("user_two")),
            (lf("superuser_client"), HTTPStatus.OK, lf("user_one")),
        ],
    )
    def test_get_user_by_id(self, client: APIClient, expected_status_code: int, user: User) -> None:
        """Проверяет получение пользователя по id."""
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
            (lf("user_one_client"), HTTPStatus.OK, lf("user_one")),
            (lf("user_one_client"), HTTPStatus.NOT_FOUND, lf("user_two")),
            (lf("superuser_client"), HTTPStatus.OK, lf("user_one")),
        ],
    )
    def test_update_user_by_id(self, client: APIClient, expected_status_code: int, user: User, faker: Faker) -> None:
        """Обновление информации о пользователе."""
        payload = {
            "username": faker.unique.user_name(),
            "email": faker.unique.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "middle_name": faker.middle_name(),
        }

        response = client.put(f"/api/v1/users/{user.id}/", payload)

        assert response.status_code == expected_status_code, "Код ответа отличается от ожидаемого"
        if expected_status_code == HTTPStatus.OK:
            user.refresh_from_db()
            assert payload["username"] == user.username, "Username пользователя не совпадает"
            assert payload["email"] == user.email, "Email пользователя не совпадает"
            assert payload["first_name"] == user.first_name, "Имя пользователя не совпадает"
            assert payload["last_name"] == user.last_name, "Фамилия пользователя не совпадает"
            assert payload["middle_name"] == user.middle_name, "Отчество пользователя не совпадает"

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, lf("user_one")),
            (lf("user_one_client"), HTTPStatus.OK, lf("user_one")),
            (lf("user_one_client"), HTTPStatus.NOT_FOUND, lf("user_two")),
            (lf("superuser_client"), HTTPStatus.OK, lf("user_one")),
        ],
    )
    def test_partial_update_user_by_id(
        self, client: APIClient, expected_status_code: int, user: User, faker: Faker
    ) -> None:
        """Частичное обновление информации о пользователе."""
        payload = {
            "username": faker.unique.user_name(),
            "email": faker.unique.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "middle_name": faker.middle_name(),
        }
        key = random.choice(list(payload.keys()))
        payload.pop(key)

        response = client.patch(f"/api/v1/users/{user.id}/", payload)

        assert response.status_code == expected_status_code, "Код ответа отличается от ожидаемого"
        if expected_status_code == HTTPStatus.OK:
            user.refresh_from_db()
            if "username" in payload:
                assert payload["username"] == user.username, "Username пользователя не совпадает"
            if "email" in payload:
                assert payload["email"] == user.email, "Email пользователя не совпадает"
            if "first_name" in payload:
                assert payload["first_name"] == user.first_name, "Имя пользователя не совпадает"
            if "last_name" in payload:
                assert payload["last_name"] == user.last_name, "Фамилия пользователя не совпадает"
            if "middle_name" in payload:
                assert payload["middle_name"] == user.middle_name, "Отчество пользователя не совпадает"

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user", "password"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, lf("user_one"), lf("user_one_password")),
            (lf("user_one_client"), HTTPStatus.NO_CONTENT, lf("user_one"), lf("user_one_password")),
            (lf("user_one_client"), HTTPStatus.FORBIDDEN, lf("user_two"), lf("user_one_password")),
            (lf("superuser_client"), HTTPStatus.NO_CONTENT, lf("user_one"), lf("superuser_password")),
        ],
    )
    def test_delete_user_by_id(self, client: APIClient, expected_status_code: int, user: User, password: str) -> None:
        """Удаление пользователя по id."""

        payload = {"current_password": password}

        response = client.delete(f"/api/v1/users/{user.id}/", payload)

        assert response.status_code == expected_status_code

        if expected_status_code == HTTPStatus.NO_CONTENT:
            user_from_db = User.objects.filter(id=user.id).first()
            assert user_from_db is None, "Пользователь не удален из базы данных"

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, None),
            (lf("user_one_client"), HTTPStatus.OK, lf("user_one")),
        ],
    )
    def test_get_user_me(self, client: APIClient, expected_status_code: int, user: User | None) -> None:
        """Проверяет получение информации о текущем пользователе."""
        response = client.get(f"/api/v1/users/me/")

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
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, None),
            (lf("user_one_client"), HTTPStatus.OK, lf("user_one")),
        ],
    )
    def test_update_user_me(
        self, client: APIClient, expected_status_code: int, user: User | None, faker: Faker
    ) -> None:
        """Обновление информации о текущем пользователе."""
        payload = {
            "username": faker.unique.user_name(),
            "email": faker.unique.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "middle_name": faker.middle_name(),
        }

        response = client.put(f"/api/v1/users/me/", payload)

        assert response.status_code == expected_status_code, "Код ответа отличается от ожидаемого"
        if expected_status_code == HTTPStatus.OK:
            user.refresh_from_db()
            assert payload["username"] == user.username, "Username пользователя не совпадает"
            assert payload["email"] == user.email, "Email пользователя не совпадает"
            assert payload["first_name"] == user.first_name, "Имя пользователя не совпадает"
            assert payload["last_name"] == user.last_name, "Фамилия пользователя не совпадает"
            assert payload["middle_name"] == user.middle_name, "Отчество пользователя не совпадает"

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, None),
            (lf("user_one_client"), HTTPStatus.OK, lf("user_one")),
        ],
    )
    def test_partial_update_user_me(
        self, client: APIClient, expected_status_code: int, user: User | None, faker: Faker, user_one_password: str
    ) -> None:
        """Частичное обновление информации о текущем пользователе."""
        payload = {
            "username": faker.unique.user_name(),
            "email": faker.unique.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "middle_name": faker.middle_name(),
        }
        key = random.choice(list(payload.keys()))
        payload.pop(key)

        response = client.patch(f"/api/v1/users/me/", payload)

        assert response.status_code == expected_status_code, "Код ответа отличается от ожидаемого"
        if expected_status_code == HTTPStatus.OK:
            user.refresh_from_db()
            if "username" in payload:
                assert payload["username"] == user.username, "Username пользователя не совпадает"
            if "email" in payload:
                assert payload["email"] == user.email, "Email пользователя не совпадает"
            if "first_name" in payload:
                assert payload["first_name"] == user.first_name, "Имя пользователя не совпадает"
            if "last_name" in payload:
                assert payload["last_name"] == user.last_name, "Фамилия пользователя не совпадает"
            if "middle_name" in payload:
                assert payload["middle_name"] == user.middle_name, "Отчество пользователя не совпадает"

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user", "password"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, None, ""),
            (lf("user_one_client"), HTTPStatus.NO_CONTENT, lf("user_one"), lf("user_one_password")),
        ],
    )
    def test_delete_user_me(
        self, client: APIClient, expected_status_code: int, user: User | None, password: str
    ) -> None:
        """Удаление текущего пользователя."""

        payload = {"current_password": password}

        response = client.delete(f"/api/v1/users/me/", payload)

        assert response.status_code == expected_status_code

        if expected_status_code == HTTPStatus.NO_CONTENT:
            user_from_db = User.objects.filter(id=user.id).first()
            assert user_from_db is None, "Пользователь не удален из базы данных"

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user", "password"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, None, ""),
            (lf("user_one_client"), HTTPStatus.NO_CONTENT, lf("user_one"), lf("user_one_password")),
        ],
    )
    def test_set_password(
        self, client: APIClient, expected_status_code: int, user: User | None, password: str, faker: Faker
    ) -> None:
        """Изменение пароля текущего пользователя."""

        payload = {
            "current_password": password,
            "new_password": faker.password(),
        }

        response = client.post(f"/api/v1/users/set_password/", payload)

        assert response.status_code == expected_status_code

        if expected_status_code == HTTPStatus.NO_CONTENT:
            user.refresh_from_db()
            assert user.check_password(payload["new_password"]), "Пароль не изменен"
