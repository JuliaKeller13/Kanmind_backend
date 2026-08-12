from django.contrib import admin

from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Configure boards for management in the Django admin."""

    list_display = ("id", "title", "owner")
    search_fields = ("title", "owner__email")
    autocomplete_fields = ("owner", "members")