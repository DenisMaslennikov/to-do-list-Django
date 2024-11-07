
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from core.models import UUIDPrimaryKeyMixin

# Create your models here.


class CustomUserManager(BaseUserManager):
    """Менеджер создания пользователей."""

    def create_user(self, email, password=None, **extra_fields):
        """Создание обычного пользователя."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, UUIDPrimaryKeyMixin):
    """Модель пользователя."""

    email = models.EmailField(unique=True, help_text="Адрес почты")
    first_name = models.CharField(max_length=30, blank=True, null=True, help_text="Имя")
    last_name = models.CharField(max_length=30, blank=True, null=True, help_text="Фамилия")
    middle_name = models.CharField(max_length=30, blank=True, null=True, help_text="Отчество")
    username = models.CharField(max_length=30, unique=True, help_text="Имя пользователя")
    is_active = models.BooleanField(default=True, help_text="Пользователь активен")
    is_staff = models.BooleanField(default=False, help_text="Пользователь является персоналом")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
