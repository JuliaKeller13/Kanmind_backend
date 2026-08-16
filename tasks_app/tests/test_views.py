from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from boards_app.models import Board
from tasks_app.models import Task

User = get_user_model()


class TaskViewSetTest(APITestCase):
    """Test task API endpoints."""

    def setUp(self):
        """Create users, a board, and authentication."""
        self.user = self._create_user("member@example.com", "Member")
        self.other_user = self._create_user("other@example.com", "Other")
        self.board = Board.objects.create(title="Project", owner=self.other_user)
        self.board.members.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.url = reverse("tasks_app:task-list")

    @staticmethod
    def _create_user(email, fullname):
        """Create a user for task endpoint tests."""
        return User.objects.create_user(
            email=email,
            password="testpassword",
            fullname=fullname,
        )

    def _valid_data(self):
        """Return valid task request data."""
        return {
            "board": self.board.id,
            "title": "Code Review",
            "description": "Review the pull request",
            "status": "review",
            "priority": "medium",
            "assignee_id": self.user.id,
            "reviewer_id": self.user.id,
            "due_date": "2026-08-20",
        }

    def test_create_task(self):
        """Create a task as a board member."""
        response = self.client.post(
            self.url,
            self._valid_data(),
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        task = Task.objects.get()
        self.assertEqual(task.board, self.board)
        self.assertEqual(task.assignee, self.user)

    def test_create_task_response(self):
        """Return the documented task response."""
        response = self.client.post(
            self.url,
            self._valid_data(),
            format="json",
        )

        self.assertEqual(
            response.data,
            self._expected_response(response.data["id"]),
        )

    def _expected_response(self, task_id):
        """Return the expected task response."""
        user_data = {
            "id": self.user.id,
            "email": self.user.email,
            "fullname": self.user.fullname,
        }
        return {
            "id": task_id,
            "board": self.board.id,
            "title": "Code Review",
            "description": "Review the pull request",
            "status": "review",
            "priority": "medium",
            "assignee": user_data,
            "reviewer": user_data,
            "due_date": "2026-08-20",
            "comments_count": 0,
        }

    def test_create_task_requires_authentication(self):
        """Reject task creation by unauthenticated users."""
        self.client.credentials()

        response = self.client.post(
            self.url,
            self._valid_data(),
            format="json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertFalse(Task.objects.exists())

    def test_create_task_requires_board_membership(self):
        """Reject task creation by non-board members."""
        self._authenticate(self.other_user)

        response = self.client.post(
            self.url,
            self._valid_data(),
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Task.objects.exists())

    def _authenticate(self, user):
        """Authenticate the API client as the given user."""
        token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

    def test_create_task_with_unknown_board(self):
        """Return not found for an unknown board ID."""
        data = self._valid_data()
        data["board"] = 999999

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Task.objects.exists())

    def test_create_task_without_board(self):
        """Reject task creation without a board."""
        data = self._valid_data()
        data.pop("board")

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Task.objects.exists())

    def test_create_task_with_invalid_assignee(self):
        """Reject an assignee who is not a board member."""
        data = self._valid_data()
        data["assignee_id"] = self.other_user.id

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Task.objects.exists())

    def test_create_task_with_invalid_board_value(self):
        """Reject an invalid board value."""
        data = self._valid_data()
        data["board"] = "abc"

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Task.objects.exists())