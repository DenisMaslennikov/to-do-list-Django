from http import HTTPStatus
import random

import pytest
from faker import Faker
from pytest_lazy_fixtures import lf
from rest_framework.test import APIClient

from classifiers.models import TaskStatus
from tasks.models import User, Task
from tests.constants import COMPLETED_TASK_STATUS_ID


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
        ("client", "expected_status_code"),
        [
            (lf("anonymous_client"), HTTPStatus.UNAUTHORIZED),
            (lf("user_one_client"), HTTPStatus.CREATED),
        ],
    )
    def test_add_task(self, client: APIClient, expected_status_code: int, faker: Faker) -> None:
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
