import uuid

from django.db import models


class UUIDPrimaryKeyMixin(models.Model):
    """Миксин для добавления первичного ключа типа UUID."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Идентификатор")

    class Meta:
        """Метакласс модели."""

        abstract = True
