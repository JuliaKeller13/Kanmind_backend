from django.contrib.auth import get_user_model
from django.test import TestCase

from boards_app.models import Board
from tasks_app.models import Comment, Task

User = get_user_model()


class TaskModelTest(TestCase):
    """Test task model behavior."""

    def test_string_representation(self):
        """Return the task title as its string representation."""
        owner = User.objects.create_user(
            email="owner@example.com",
            password="testpassword",
            fullname="Board Owner",
        )
        board = Board.objects.create(
            title="Project",
            owner=owner,
        )
        task = Task.objects.create(
            board=board,
            title="Code Review",
            description="Review code",
            status=Task.Status.REVIEW,
            priority=Task.Priority.MEDIUM,
            due_date="2026-08-20",
        )

        self.assertEqual(str(task), "Code Review")

    def test_comment_string_representation(self):
        """Return the comment content as its string representation."""
        owner = User.objects.create_user(
            email="comment@example.com",
            password="testpassword",
            fullname="Comment Author",
        )
        board = Board.objects.create(
            title="Project",
            owner=owner,
        )
        task = Task.objects.create(
            board=board,
            created_by=owner,
            title="Task",
            description="Description",
            status=Task.Status.TO_DO,
            priority=Task.Priority.LOW,
            due_date="2026-08-20",
        )
        comment = Comment.objects.create(
            task=task,
            author=owner,
            content="Test comment",
        )

        self.assertEqual(str(comment), "Test comment")