from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.tasks.filters import TaskFilter
from api.v1.tasks.permissions import IsTaskOwnerOrForbidden
from api.v1.tasks.serializers import TaskListSerializer, TaskSerializer, TaskStatusUpdateSerializer, TaskWriteSerializer
from tasks.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    """Вьюсет задач."""

    permission_classes = [IsTaskOwnerOrForbidden, permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    ordering_fields = "__all__"
    filterset_class = TaskFilter

    def get_queryset(self):
        """Получение кверисета с фильтрацией по пользователю."""
        if not self.request.user.is_authenticated:
            return Task.objects.none()
        return Task.objects.filter(user=self.request.user).select_related("task_status")

    def get_serializer_class(self):
        """Получение класса сериализатора в зависимости от типа запроса."""
        if self.action == "list":
            return TaskListSerializer
        elif self.action == "retrieve":
            return TaskSerializer
        return TaskWriteSerializer

    def perform_create(self, serializer):
        """Создание задачи."""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Обновление задачи."""
        serializer.save(user=self.request.user)

    @extend_schema(request=TaskStatusUpdateSerializer, responses={status.HTTP_200_OK: TaskSerializer})
    @action(detail=True, methods=["PATCH"], serializer_class=TaskStatusUpdateSerializer)
    def change_status(self, request, pk=None):
        """Обновление статуса задачи."""
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        response_serializer = TaskSerializer(task)
        if serializer.is_valid():
            serializer.save()
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
