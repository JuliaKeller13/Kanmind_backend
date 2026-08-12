from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Board

User = get_user_model()


class BoardSerializer(serializers.ModelSerializer):
    """Serialize board creation and board response data."""

    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
    )
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = (
            "id",
            "title",
            "members",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        )

    def get_member_count(self, board):
        """Return the number of members assigned to the board."""
        return board.members.count()

    def get_ticket_count(self, board):
        """Return the number of tasks on a newly created board."""
        return 0

    def get_tasks_to_do_count(self, board):
        """Return the number of to-do tasks on a newly created board."""
        return 0

    def get_tasks_high_prio_count(self, board):
        """Return the number of high-priority tasks on a new board."""
        return 0