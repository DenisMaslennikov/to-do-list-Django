from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserSerializer

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя."""

    last_login = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "is_active",
            "last_login",
        )
