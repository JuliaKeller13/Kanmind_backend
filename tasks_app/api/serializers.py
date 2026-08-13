from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Task

User = get_user_model()


class TaskUserSerializer(serializers.ModelSerializer):
    """Serialize basic user information for task relations."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullname",
        )


class TaskSerializer(serializers.ModelSerializer):
    """Serialize task creation and task response data."""

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        allow_null=True,
        required=False,
        write_only=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        allow_null=True,
        required=False,
        write_only=True,
    )
    assignee = TaskUserSerializer(read_only=True)
    reviewer = TaskUserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "reviewer_id",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        )

    def validate(self, attrs):
        """Ensure assignee and reviewer belong to the selected board."""
        board = attrs.get("board")
        self._validate_board_member(board, attrs.get("assignee"), "assignee_id")
        self._validate_board_member(board, attrs.get("reviewer"), "reviewer_id")
        return attrs

    @staticmethod
    def _validate_board_member(board, user, field):
        """Ensure a task user belongs to the selected board."""
        if user is not None and not board.members.filter(id=user.id).exists():
            raise serializers.ValidationError(
                {field: "User must be a member of the board."}
            )

    def get_comments_count(self, task):
        """Return the number of comments assigned to the task."""
        return 0