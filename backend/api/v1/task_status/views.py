from rest_framework import mixins, permissions, viewsets

from api.v1.task_status.serializers import TaskStatusSerializer
from classifiers.models import TaskStatus


class TaskStatusViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Вьюсет списка статусов."""

    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    permission_classes = (permissions.AllowAny,)
