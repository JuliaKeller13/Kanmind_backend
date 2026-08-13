from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Configure tasks for management in the Django admin."""

    list_display = (
        "id",
        "title",
        "board",
        "status",
        "priority",
        "assignee",
        "reviewer",
        "due_date",
    )
    list_filter = ("status", "priority")
    search_fields = (
        "title",
        "board__title",
        "assignee__email",
        "reviewer__email",
    )
    autocomplete_fields = (
        "board",
        "assignee",
        "reviewer",
    )