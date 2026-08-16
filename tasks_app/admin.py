from django.contrib import admin

from .models import Comment, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Configure tasks for management in the Django admin."""

    list_display = (
        "id",
        "title",
        "board",
        "created_by",
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
        "created_by__email",
        "assignee__email",
        "reviewer__email",
    )
    autocomplete_fields = (
        "board",
        "assignee",
        "reviewer",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Configure comments for management in the Django admin."""

    list_display = (
        "id",
        "task",
        "author",
        "created_at",
    )
    search_fields = (
        "content",
        "author__email",
        "task__title",
    )
    autocomplete_fields = ("task", "author")
    readonly_fields = ("created_at",)