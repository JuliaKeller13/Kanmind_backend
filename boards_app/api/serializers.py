from django.contrib.auth import get_user_model
from rest_framework import serializers

from tasks_app.models import Task

from ..models import Board

User = get_user_model()


class BoardMemberSerializer(serializers.ModelSerializer):
    """Serialize basic user information for board members."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullname",
        )

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
        """Return the total number of tasks on the board."""
        return board.tasks.count()

    def get_tasks_to_do_count(self, board):
        """Return the number of to-do tasks on the board."""
        return board.tasks.filter(
            status=Task.Status.TO_DO,
        ).count()

    def get_tasks_high_prio_count(self, board):
        """Return the number of high-priority tasks on the board."""
        return board.tasks.filter(
            priority=Task.Priority.HIGH,
        ).count()

class BoardTaskSerializer(serializers.ModelSerializer):
    """Serialize task information inside a board detail response."""

    assignee = BoardMemberSerializer(read_only=True)
    reviewer = BoardMemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        )

    def get_comments_count(self, task):
        """Return the number of comments assigned to the task."""
        return task.comments.count()

class BoardDetailSerializer(serializers.ModelSerializer):
    """Serialize detailed board information."""

    members = BoardMemberSerializer(
        many=True,
        read_only=True,
    )
    tasks = BoardTaskSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Board
        fields = (
            "id",
            "title",
            "owner_id",
            "members",
            "tasks",
        )

class BoardUpdateSerializer(serializers.ModelSerializer):
    """Serialize board updates and updated board data."""

    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
    )
    owner_data = BoardMemberSerializer(
        source="owner",
        read_only=True,
    )
    members_data = BoardMemberSerializer(
        source="members",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Board
        fields = (
            "id",
            "title",
            "members",
            "owner_data",
            "members_data",
        )

class EmailCheckSerializer(serializers.Serializer):
    """Validate the email query parameter."""

    email = serializers.EmailField()