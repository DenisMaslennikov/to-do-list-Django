from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.v1.task_status.views import TaskStatusViewSet

router = DefaultRouter()
router.register("task_statuses", TaskStatusViewSet, basename="task_statuses")
# router.register("users", CustomUserViewSet)

app_name = "v1"

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
]
