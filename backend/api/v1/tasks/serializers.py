from rest_framework import serializers

from api.v1.task_status.serializers import TaskStatusSerializer
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор задачи для детального отображения."""

    task_status = TaskStatusSerializer(read_only=True)

    class Meta:
        """Метакласс сериализатора задач."""

        model = Task
        fields = ("title", "description", "task_status", "created_at", "updated_at", "complete_before", "completed_at")
        read_only_fields = ("created_at", "updated_at")


class TaskWriteSerializer(serializers.ModelSerializer):
    """Сериализатор задач для операций записи."""

    class Meta:
        """Метакласс сериализатора записи для задач."""

        model = Task
        fields = ("title", "description", "task_status", "created_at", "updated_at", "complete_before", "completed_at")
        read_only_fields = ("created_at", "updated_at")


class TaskListSerializer(serializers.ModelSerializer):
    """Сериализатор задач для представления в списках."""

    task_status = TaskStatusSerializer(read_only=True)

    class Meta:
        """Метакласс сериализатора задач."""

        model = Task
        fields = ("id", "title", "task_status", "complete_before", "completed_at")


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    """Серилазиатор статуса задач."""

    class Meta:
        """Метакласс сериализатора."""

        model = Task
        fields = ("task_status",)
