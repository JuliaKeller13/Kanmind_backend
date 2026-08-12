from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from boards_app.models import Board

User = get_user_model()


class BoardViewSetTest(APITestCase):
    """Test board API endpoints."""

    def setUp(self):
        """Create authenticated users for board endpoint tests."""
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
        self.token = Token.objects.create(user=self.owner)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.url = reverse("boards_app:board-list")

    def test_create_board(self):
        """Create a board for the authenticated user."""
        data = {
            "title": "New Project",
            "members": [self.member.id],
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 201)
        board = Board.objects.get()
        self.assertEqual(board.owner, self.owner)
        self.assertIn(self.member, board.members.all())

    def test_create_board_response(self):
        """Return the documented response after board creation."""
        data = {
            "title": "New Project",
            "members": [self.member.id],
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(
            response.data,
            {
                "id": response.data["id"],
                "title": "New Project",
                "member_count": 1,
                "ticket_count": 0,
                "tasks_to_do_count": 0,
                "tasks_high_prio_count": 0,
                "owner_id": self.owner.id,
            },
        )

    def test_create_board_requires_authentication(self):
        """Reject board creation by unauthenticated users."""
        self.client.credentials()

        response = self.client.post(
            self.url,
            {"title": "New Project", "members": []},
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_create_board_with_invalid_member(self):
        """Reject board creation with an unknown member ID."""
        data = {
            "title": "New Project",
            "members": [999999],
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Board.objects.exists())