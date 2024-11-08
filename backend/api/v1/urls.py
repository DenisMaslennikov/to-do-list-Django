from django.urls import include, path

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register("users", CustomUserViewSet)

app_name = "v1"

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
