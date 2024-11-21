import random
from datetime import datetime, timedelta
from http import HTTPStatus
from http.client import responses

import pytest
from django.db.models.functions import Random
from faker import Faker
from pytest_lazy_fixtures import lf
from rest_framework.test import APIClient

from classifiers.models import TaskStatus
from tasks.models import Task, User
from tests.constants import COMPLETED_TASK_STATUS_ID
from tests.functions import date_format, date_from_iso_str


@pytest.mark.django_db
class TestTaskApi:
    """Класс тестов АПИ задач."""

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, None),
            (lf("user_one_client"), HTTPStatus.OK, lf("user_one")),
            (lf("user_two_client"), HTTPStatus.OK, lf("user_two")),
        ],
    )
    @pytest.mark.usefixtures("user_one_tasks")
    def test_get_task_list(self, client: APIClient, expected_status_code: int, user: User | None) -> None:
        """Проверяет получение списка задач в зависимости от пользователя."""
        response = client.get("/api/v1/tasks/")
        assert response.status_code == expected_status_code, "Код ответа отличается от ожидаемого"

        if expected_status_code == HTTPStatus.OK:
            json = response.json()
            assert len(json) == user.tasks.count()

    @pytest.mark.parametrize(
        ("client", "expected_status_code", "user"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED, None),
            (lf("user_one_client"), HTTPStatus.CREATED, lf("user_one")),
        ],
    )
    def test_add_task(self, client: APIClient, expected_status_code: int, user: User, faker: Faker) -> None:
        """Проверяет создание задачи."""
        tasks_status: list[TaskStatus] = TaskStatus.objects.all()
        task_status = random.choice(tasks_status)
        completed_at = None
        complete_before = None
        if task_status.id == COMPLETED_TASK_STATUS_ID:
            completed_at = faker.date_time()
        if faker.boolean(75):
            complete_before = faker.date_time()
        payload = {
            "title": faker.text(max_nb_chars=50),
            "description": faker.text(max_nb_chars=500),
            "task_status": task_status.id,
        }
        if completed_at is not None:
            payload["completed_at"] = completed_at
        if complete_before is not None:
            payload["complete_before"] = complete_before
        response = client.post("/api/v1/tasks/", data=payload)

        assert response.status_code == expected_status_code, "Код ответа отличается от ожидаемого"

        if expected_status_code == HTTPStatus.CREATED:
            assert Task.objects.count() == 1, "Количество задач в базе отличается от ожидаемого"
            task_from_bd: Task = Task.objects.all().first()
            assert task_from_bd.user == user, "Пользователь создавший задачу не соответствует ожидаемому"
            assert task_from_bd.title == payload["title"], "Заголовок задачи не соответствует переданному"
            assert task_from_bd.description == payload["description"], "Описание задачи не соответствует переданному"
            assert task_from_bd.task_status == task_status, "Статус задачи не соответствует переданному"
            if completed_at is not None:
                assert (
                    task_from_bd.completed_at.timestamp() == completed_at.timestamp()
                ), "Время выполнения задачи не соответствует переданному"
            if complete_before is not None:
                assert (
                    task_from_bd.complete_before.timestamp() == complete_before.timestamp()
                ), "Время выполнить до не соответствует переданному"
            assert (
                task_from_bd.updated_at.timestamp() < datetime.now().timestamp()
                and task_from_bd.updated_at.timestamp() > (datetime.now() - timedelta(seconds=1)).timestamp()
            ), "Время последнего изменения задачи не соответствует ожидаемому"

            assert (
                task_from_bd.created_at.timestamp() < datetime.now().timestamp()
                and task_from_bd.created_at.timestamp() > (datetime.now() - timedelta(seconds=1)).timestamp()
            ), "Время создание задачи не соответствует ожидаемому"

    @pytest.mark.parametrize(
        ("client", "expected_status_code"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED),
            (lf("user_one_client"), HTTPStatus.OK),
            (lf("user_two_client"), HTTPStatus.NOT_FOUND),
        ],
    )
    def test_get_task_by_id(self, client: APIClient, expected_status_code: int, user_one_task: Task) -> None:
        """Проверяет получение задачи по id."""
        response = client.get(f"/api/v1/tasks/{user_one_task.id}/")
        assert response.status_code == expected_status_code
        if expected_status_code == HTTPStatus.OK:
            json = response.json()
            assert json["title"] == user_one_task.title, "Заголовок задачи не совпадает"
            assert json["description"] == user_one_task.description, "Описание задачи не совпадает"
            assert json["task_status"]["id"] == user_one_task.task_status.id, "Статус задачи не совпадает"
            model_created_at = date_format(user_one_task.created_at)
            api_created_at = date_from_iso_str(json["created_at"])
            assert api_created_at == model_created_at, "Время создание задачи не совпадает"
            model_updated_at = date_format(user_one_task.updated_at)
            api_updated_at = date_from_iso_str(json["updated_at"])
            assert api_updated_at == model_updated_at, "Время обновления задачи не совпадает"
            model_complete_before = date_format(user_one_task.complete_before)
            api_complete_before = date_from_iso_str(json["complete_before"])
            assert api_complete_before == model_complete_before, "Время завершить до не совпадает"
            model_completed_at = date_format(user_one_task.completed_at)
            api_completed_at = date_from_iso_str(json["completed_at"])
            assert api_completed_at == model_completed_at, "Время завершения задачи не совпадает"

    @pytest.mark.parametrize(
        ("client", "expected_status_code"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED),
            (lf("user_one_client"), HTTPStatus.OK),
            (lf("user_two_client"), HTTPStatus.NOT_FOUND),
        ],
    )
    def test_update_task_by_id(
        self, client: APIClient, expected_status_code: int, user_one_task: Task, faker: Faker
    ) -> None:
        """Проверка обновления задачи по id."""
        tasks_status: list[TaskStatus] = TaskStatus.objects.all()
        task_status = random.choice(tasks_status)
        completed_at = None
        complete_before = None
        if task_status.id == COMPLETED_TASK_STATUS_ID:
            completed_at = faker.date_time()
        if faker.boolean(75):
            complete_before = faker.date_time()
        payload = {
            "title": faker.text(max_nb_chars=50),
            "description": faker.text(max_nb_chars=500),
            "task_status": task_status.id,
        }
        if completed_at is not None:
            payload["completed_at"] = completed_at
        else:
            payload["completed_at"] = ""
        if complete_before is not None:
            payload["complete_before"] = complete_before
        else:
            payload["complete_before"] = ""

        response = client.put(f"/api/v1/tasks/{user_one_task.id}/", data=payload)
        assert response.status_code == expected_status_code
        if expected_status_code == HTTPStatus.OK:
            user_one_task.refresh_from_db()
            assert user_one_task.title == payload["title"], "Заголовок задачи не совпадает"
            assert user_one_task.description == payload["description"], "Описание задачи не совпадает"
            assert user_one_task.task_status.id == payload["task_status"], "Статус задачи не совпадает"
            if completed_at is not None:
                assert (
                    user_one_task.completed_at.timestamp() == completed_at.timestamp()
                ), "Время завершения не совпадает"
            else:
                assert user_one_task.completed_at is None, "Время завершения не совпадает"
            if complete_before is not None:
                assert (
                    user_one_task.complete_before.timestamp() == complete_before.timestamp()
                ), "Время выполнить до не совпадает"
            else:
                assert user_one_task.complete_before is None, "Время выполнить до не совпадает"

    @pytest.mark.parametrize(
        ("client", "expected_status_code"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED),
            (lf("user_one_client"), HTTPStatus.OK),
            (lf("user_two_client"), HTTPStatus.NOT_FOUND),
        ],
    )
    def test_partial_update_task_by_id(
        self, client: APIClient, expected_status_code: int, user_one_task: Task, faker: Faker
    ) -> None:
        """Проверка обновления задачи по id."""
        tasks_status: list[TaskStatus] = TaskStatus.objects.all()
        task_status = random.choice(tasks_status)
        completed_at = None
        complete_before = None
        if task_status.id == COMPLETED_TASK_STATUS_ID:
            completed_at = faker.date_time()
        if faker.boolean(75):
            complete_before = faker.date_time()
        payload = {
            "title": faker.text(max_nb_chars=50),
            "description": faker.text(max_nb_chars=500),
            "task_status": task_status.id,
        }
        if completed_at is not None:
            payload["completed_at"] = completed_at
        else:
            payload["completed_at"] = ""
        if complete_before is not None:
            payload["complete_before"] = complete_before
        else:
            payload["complete_before"] = ""

        key = random.choice(list(payload.keys()))
        payload.pop(key)
        old_value = getattr(user_one_task, key)

        response = client.patch(f"/api/v1/tasks/{user_one_task.id}/", data=payload)
        assert response.status_code == expected_status_code
        if expected_status_code == HTTPStatus.OK:
            user_one_task.refresh_from_db()
            if "title" in payload:
                assert user_one_task.title == payload["title"], "Заголовок задачи не совпадает"
            else:
                assert user_one_task.title == old_value, "Заголовок был изменен хотя не передавался"
            if "description" in payload:
                assert user_one_task.description == payload["description"], "Описание задачи не совпадает"
            else:
                assert user_one_task.description == old_value, "Описание задачи было изменено хотя не передавалось"
            if "task_status" in payload:
                assert user_one_task.task_status.id == payload["task_status"], "Статус задачи не совпадает"
            else:
                assert user_one_task.task_status == old_value, "Статус задачи был изменен хотя не передавался"
            if "completed_at" in payload:
                if completed_at is not None:
                    assert (
                        user_one_task.completed_at.timestamp() == completed_at.timestamp()
                    ), "Время завершения не совпадает"
                else:
                    assert user_one_task.completed_at is None, "Время завершения не совпадает"
            else:
                assert user_one_task.completed_at == old_value, "Время выполнение было изменено хотя не передавалось"
            if "complete_before" in payload:
                if complete_before is not None:
                    assert (
                        user_one_task.complete_before.timestamp() == complete_before.timestamp()
                    ), "Время выполнить до не совпадает"
                else:
                    assert user_one_task.complete_before is None, "Время выполнить до не совпадает"
            else:
                assert (
                    user_one_task.complete_before == old_value
                ), "Время выполнить до было изменено хотя не передавалось"

    @pytest.mark.parametrize(
        ("client", "expected_status_code"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED),
            (lf("user_one_client"), HTTPStatus.NO_CONTENT),
            (lf("user_two_client"), HTTPStatus.NOT_FOUND),
        ],
    )
    def test_delete_task_by_id(self, client: APIClient, expected_status_code: int, user_one_task: Task) -> None:
        """Удаление задачи по id."""
        response = client.delete(f"/api/v1/tasks/{user_one_task.id}/")
        assert response.status_code == expected_status_code
        if expected_status_code == HTTPStatus.NO_CONTENT:
            task_from_bd = Task.objects.filter(id=user_one_task.id).first()
            assert task_from_bd is None, "Задача не была удалена из бд"

    @pytest.mark.parametrize(
        ("client", "expected_status_code"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED),
            (lf("user_one_client"), HTTPStatus.OK),
            (lf("user_two_client"), HTTPStatus.NOT_FOUND),
        ],
    )
    def test_update_task_status(self, client: APIClient, expected_status_code: int, user_one_task: Task) -> None:
        """Обновление статуса задачи."""
        task_status = TaskStatus.objects.exclude(id=user_one_task.task_status.id).order_by(Random()).first()
        payload = {
            "task_status": task_status.id,
        }
        response = client.patch(f"/api/v1/tasks/{user_one_task.id}/change_status/", data=payload)
        assert response.status_code == expected_status_code
        if expected_status_code == HTTPStatus.OK:
            user_one_task.refresh_from_db()
            assert user_one_task.task_status.id == payload["task_status"], "Статус задачи не был изменен"
