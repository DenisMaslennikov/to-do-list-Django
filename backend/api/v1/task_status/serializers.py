from rest_framework import serializers

from classifiers.models import TaskStatus


class TaskStatusSerializer(serializers.ModelSerializer):
    """Сериализатор статуса задач."""

    class Meta:
        model = TaskStatus
        fields = "__all__"
