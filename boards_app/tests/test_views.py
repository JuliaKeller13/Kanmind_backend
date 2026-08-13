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

    def get_detail_url(self, board):
        """Return the detail URL for a board."""
        return reverse(
            "boards_app:board-detail",
            kwargs={"board_id": board.id},
        )

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

    def test_list_accessible_boards(self):
        """Return boards owned by or assigned to the authenticated user."""
        owned_board = Board.objects.create(
            title="Owned Board",
            owner=self.owner,
        )
        member_board = Board.objects.create(
            title="Member Board",
            owner=self.member,
        )
        member_board.members.add(self.owner)

        other_user = User.objects.create_user(
            email="other@example.com",
            password="testpassword",
            fullname="Other User",
        )
        Board.objects.create(
            title="Private Board",
            owner=other_user,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        board_ids = {board["id"] for board in response.data}
        self.assertEqual(
            board_ids,
            {owned_board.id, member_board.id},
        )

    def test_list_does_not_duplicate_owned_member_board(self):
        """Return a board once when the owner is also a member."""
        board = Board.objects.create(
            title="Shared Board",
            owner=self.owner,
        )
        board.members.add(self.owner)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], board.id)

    def test_list_boards_requires_authentication(self):
        """Reject board listing by unauthenticated users."""
        self.client.credentials()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)

    def test_retrieve_board_as_owner(self):
        """Allow the owner to retrieve board details."""
        board = Board.objects.create(
            title="Owned Board",
            owner=self.owner,
        )
        board.members.add(self.member)

        response = self.client.get(self.get_detail_url(board))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], board.id)
        self.assertEqual(response.data["title"], "Owned Board")
        self.assertEqual(response.data["owner_id"], self.owner.id)

    def test_retrieve_board_without_access(self):
        """Reject users who are neither owner nor board member."""
        other_user = User.objects.create_user(
            email="other@example.com",
            password="testpassword",
            fullname="Other User",
        )
        board = Board.objects.create(
            title="Private Board",
            owner=other_user,
        )

        response = self.client.get(self.get_detail_url(board))

        self.assertEqual(response.status_code, 403)

    def test_retrieve_unknown_board(self):
        """Return not found for an unknown board ID."""
        url = reverse(
            "boards_app:board-detail",
            kwargs={"board_id": 999999},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_retrieve_board_response_data(self):
        """Return members and task data in the board detail response."""
        board = Board.objects.create(
            title="Project X",
            owner=self.owner,
        )
        board.members.add(self.member)

        response = self.client.get(self.get_detail_url(board))

        self.assertEqual(
            response.data,
            {
                "id": board.id,
                "title": "Project X",
                "owner_id": self.owner.id,
                "members": [
                    {
                        "id": self.member.id,
                        "email": self.member.email,
                        "fullname": self.member.fullname,
                    }
                ],
                "tasks": [],
            },
        )