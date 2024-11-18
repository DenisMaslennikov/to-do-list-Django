from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from classifiers.models import TaskStatus


@pytest.mark.django_db
def test_get_task_status_classifier(anonymous_client: APIClient) -> None:
    """Проверяет получение классификатора статусов задач."""
    response = anonymous_client.get("/api/v1/task_statuses/")
    assert response.status_code == HTTPStatus.OK, "Код ответа не соответствует ожидаемому"
    assert (
        len(response.json()) == TaskStatus.objects.count()
    ), "Количество результатов в ответе не соответствует ожидаемому"
