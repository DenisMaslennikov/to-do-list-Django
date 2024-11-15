# Generated by Django 5.1.3 on 2024-11-08 09:45

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, help_text="Идентификатор", primary_key=True, serialize=False
                    ),
                ),
                ("email", models.EmailField(help_text="Адрес почты", max_length=254, unique=True)),
                ("first_name", models.CharField(blank=True, help_text="Имя", max_length=30, null=True)),
                ("last_name", models.CharField(blank=True, help_text="Фамилия", max_length=30, null=True)),
                ("middle_name", models.CharField(blank=True, help_text="Отчество", max_length=30, null=True)),
                ("username", models.CharField(help_text="Имя пользователя", max_length=30, unique=True)),
                ("is_active", models.BooleanField(default=True, help_text="Пользователь активен")),
                ("is_staff", models.BooleanField(default=False, help_text="Пользователь является персоналом")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
