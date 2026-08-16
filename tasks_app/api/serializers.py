from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Comment, Task

User = get_user_model()


def validate_board_member(board, user, field):
    """Ensure a task user belongs to the selected board."""
    if user is not None and not board.members.filter(id=user.id).exists():
        raise serializers.ValidationError(
            {field: "User must be a member of the board."}
        )


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
        validate_board_member(board, attrs.get("assignee"), "assignee_id")
        validate_board_member(board, attrs.get("reviewer"), "reviewer_id")
        return attrs

    def get_comments_count(self, task):
        """Return the number of comments assigned to the task."""
        return task.comments.count()


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Serialize partial task updates."""

    board = serializers.IntegerField(
        write_only=True,
        required=False,
    )
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
        )

    def validate_board(self, value):
        """Reject attempts to change the task board."""
        raise serializers.ValidationError(
            "Changing the board is not allowed."
        )

    def validate(self, attrs):
        """Ensure task users remain members of the task board."""
        board = self.instance.board
        validate_board_member(board, attrs.get("assignee"), "assignee_id")
        validate_board_member(board, attrs.get("reviewer"), "reviewer_id")
        return attrs

class CommentSerializer(serializers.ModelSerializer):
    """Serialize task comments."""

    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "created_at",
            "author",
            "content",
        )
        read_only_fields = (
            "id",
            "created_at",
            "author",
        )

    def get_author(self, comment):
        """Return the comment author's full name."""
        if comment.author is None:
            return None
        return comment.author.fullname