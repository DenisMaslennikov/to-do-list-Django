# Generated by Django 5.1.3 on 2024-11-07 12:21

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("classifiers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, help_text="Идентификатор", primary_key=True, serialize=False
                    ),
                ),
                ("title", models.CharField(help_text="Заголовок задачи", max_length=100)),
                ("description", models.TextField(help_text="Описание задачи")),
                ("created_at", models.DateTimeField(auto_now_add=True, help_text="Создана")),
                ("updated_at", models.DateTimeField(auto_now=True, help_text="Обновлена")),
                ("complete_before", models.DateTimeField(blank=True, help_text="Завершить до", null=True)),
                ("completed_at", models.DateTimeField(blank=True, help_text="Завершена", null=True)),
                (
                    "task_status_id",
                    models.ForeignKey(
                        help_text="Статус задачи",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="tasks",
                        to="classifiers.taskstatus",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]