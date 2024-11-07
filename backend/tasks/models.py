from django.contrib.auth import get_user_model
from django.db import models

from classifiers.models import TaskStatus
from core.models import UUIDPrimaryKeyMixin

User = get_user_model()


class Task(UUIDPrimaryKeyMixin, models.Model):
    """Модель задачи."""

    title = models.CharField(max_length=100, help_text="Заголовок задачи")
    description = models.TextField(help_text="Описание задачи")
    task_status_id = models.ForeignKey(
        TaskStatus, on_delete=models.PROTECT, help_text="Статус задачи", related_name="tasks"
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Пользователь", related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Создана")
    updated_at = models.DateTimeField(auto_now=True, help_text="Обновлена")
    complete_before = models.DateTimeField(help_text="Завершить до", null=True, blank=True)
    completed_at = models.DateTimeField(help_text="Завершена", null=True, blank=True)

    def __str__(self):
        return self.title
