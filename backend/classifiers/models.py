from django.db import models

# Create your models here.


class TaskStatus(models.Model):
    """Классификатор статусов задачи."""

    name = models.CharField(max_length=100, unique=True)
