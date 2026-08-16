from django.contrib.auth import get_user_model
from django.test import TestCase

from boards_app.models import Board
from tasks_app.api.serializers import CommentSerializer, TaskSerializer
from tasks_app.models import Comment, Task

User = get_user_model()


class TaskSerializerTest(TestCase):
    """Test task serializer validation and creation."""

    def setUp(self):
        """Create board users for serializer tests."""
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="testpassword",
            fullname="Board Owner",
        )
        self.member = User.objects.create_user(
            email="member@example.com",
            password="testpassword",
            fullname="Board Member",
        )
        self.board = Board.objects.create(
            title="Project",
            owner=self.owner,
        )
        self.board.members.add(self.member)

    def test_create_task_with_valid_members(self):
        """Create a task with valid assignee and reviewer."""
        data = {
            "board": self.board.id,
            "title": "Code Review",
            "description": "Review the pull request",
            "status": "review",
            "priority": "medium",
            "assignee_id": self.member.id,
            "reviewer_id": self.member.id,
            "due_date": "2026-08-20",
        }

        serializer = TaskSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        task = serializer.save()

        self.assertEqual(task.board, self.board)
        self.assertEqual(task.assignee, self.member)
        self.assertEqual(task.reviewer, self.member)

    def test_reject_invalid_status(self):
        """Reject unsupported task status values."""
        data = {
            "board": self.board.id,
            "title": "Task",
            "description": "Description",
            "status": "waiting",
            "priority": "medium",
            "due_date": "2026-08-20",
        }

        serializer = TaskSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)

    def test_reject_invalid_priority(self):
        """Reject unsupported priority values."""
        data = {
            "board": self.board.id,
            "title": "Task",
            "description": "Description",
            "status": "to-do",
            "priority": "urgent",
            "due_date": "2026-08-20",
        }

        serializer = TaskSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("priority", serializer.errors)

    def test_reject_assignee_outside_board(self):
        """Reject assignees who are not board members."""
        outsider = User.objects.create_user(
            email="outsider@example.com",
            password="testpassword",
            fullname="Outsider",
        )
        data = {
            "board": self.board.id,
            "title": "Task",
            "description": "Description",
            "status": "to-do",
            "priority": "high",
            "assignee_id": outsider.id,
            "due_date": "2026-08-20",
        }

        serializer = TaskSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("assignee_id", serializer.errors)

    def test_reject_reviewer_outside_board(self):
        """Reject reviewers who are not board members."""
        outsider = User.objects.create_user(
            email="reviewer@example.com",
            password="testpassword",
            fullname="Outsider Reviewer",
        )
        data = {
            "board": self.board.id,
            "title": "Task",
            "description": "Description",
            "status": "to-do",
            "priority": "high",
            "reviewer_id": outsider.id,
            "due_date": "2026-08-20",
        }

        serializer = TaskSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("reviewer_id", serializer.errors)

    def test_allow_empty_assignee_and_reviewer(self):
        """Allow task creation without assignee or reviewer."""
        data = {
            "board": self.board.id,
            "title": "Unassigned Task",
            "description": "Description",
            "status": "to-do",
            "priority": "low",
            "due_date": "2026-08-20",
        }

        serializer = TaskSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        task = serializer.save()

        self.assertIsNone(task.assignee)
        self.assertIsNone(task.reviewer)

    def test_comment_serializer_without_author(self):
        """Return null when a comment has no author."""
        task = self._create_task()
        comment = Comment.objects.create(
            task=task,
            author=None,
            content="Anonymous comment",
        )

        serializer = CommentSerializer(comment)

        self.assertIsNone(serializer.data["author"])

    def _create_task(self):
        """Create a task for serializer tests."""
        return Task.objects.create(
            board=self.board,
            created_by=self.owner,
            title="Test Task",
            description="Test description",
            status=Task.Status.TO_DO,
            priority=Task.Priority.LOW,
            due_date="2026-08-20",
        )