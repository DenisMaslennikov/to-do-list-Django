from django_filters.rest_framework import FilterSet, IsoDateTimeFromToRangeFilter, ModelChoiceFilter

from classifiers.models import TaskStatus
from tasks.models import Task


class TaskFilter(FilterSet):
    task_status = ModelChoiceFilter(queryset=TaskStatus.objects.all())
    created_at = IsoDateTimeFromToRangeFilter(field_name="created_at")
    updated_at = IsoDateTimeFromToRangeFilter()
    complete_before = IsoDateTimeFromToRangeFilter()
    completed_at = IsoDateTimeFromToRangeFilter()

    class Meta:
        model = Task
        fields = ("task_status", "created_at", "updated_at", "complete_before", "completed_at")