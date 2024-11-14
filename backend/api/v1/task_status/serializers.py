from rest_framework import serializers

from classifiers.models import TaskStatus


class TaskStatusSerializer(serializers.ModelSerializer):
    """Сериализатор статуса задач."""

    class Meta:
        """Меакласс сериализатора статусов задач."""

        model = TaskStatus
        fields = "__all__"
