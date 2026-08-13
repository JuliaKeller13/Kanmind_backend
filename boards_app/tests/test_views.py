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
        self.email_check_url = reverse("boards_app:email-check")

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

    def test_update_board_as_owner(self):
        """Allow the owner to update title and members."""
        board = Board.objects.create(
            title="Old title",
            owner=self.owner,
        )

        response = self.client.patch(
            self.get_detail_url(board),
            {
                "title": "Changed title",
                "members": [self.member.id],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        board.refresh_from_db()
        self.assertEqual(board.title, "Changed title")
        self.assertIn(self.member, board.members.all())

    def test_update_board_as_member(self):
        """Allow a board member to update the board."""
        board = Board.objects.create(
            title="Member Board",
            owner=self.member,
        )
        board.members.add(self.owner)

        response = self.client.patch(
            self.get_detail_url(board),
            {"title": "Updated by member"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        board.refresh_from_db()
        self.assertEqual(board.title, "Updated by member")

    def test_update_replaces_members(self):
        """Replace existing members with the submitted member list."""
        second_member = User.objects.create_user(
            email="second@example.com",
            password="testpassword",
            fullname="Second Member",
        )
        board = Board.objects.create(
            title="Board",
            owner=self.owner,
        )
        board.members.add(self.member, second_member)

        response = self.client.patch(
            self.get_detail_url(board),
            {"members": [self.member.id]},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(board.members.values_list("id", flat=True)),
            [self.member.id],
        )

    def test_update_board_with_invalid_member(self):
        """Reject an unknown member ID."""
        board = Board.objects.create(
            title="Board",
            owner=self.owner,
        )

        response = self.client.patch(
            self.get_detail_url(board),
            {"members": [999999]},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_board_requires_authentication(self):
        """Reject board updates by unauthenticated users."""
        board = Board.objects.create(
            title="Board",
            owner=self.owner,
        )
        self.client.credentials()

        response = self.client.patch(
            self.get_detail_url(board),
            {"title": "Changed"},
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_update_board_without_access(self):
        """Reject updates by users without board access."""
        other_user = User.objects.create_user(
            email="other@example.com",
            password="testpassword",
            fullname="Other User",
        )
        board = Board.objects.create(
            title="Private Board",
            owner=other_user,
        )

        response = self.client.patch(
            self.get_detail_url(board),
            {"title": "Changed"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_update_unknown_board(self):
        """Return not found for an unknown board ID."""
        url = reverse(
            "boards_app:board-detail",
            kwargs={"board_id": 999999},
        )

        response = self.client.patch(
            url,
            {"title": "Changed"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_update_board_response_data(self):
        """Return owner and member data after an update."""
        board = Board.objects.create(
            title="Old title",
            owner=self.owner,
        )

        response = self.client.patch(
            self.get_detail_url(board),
            {
                "title": "Changed title",
                "members": [self.member.id],
            },
            format="json",
        )

        self.assertEqual(
            response.data,
            {
                "id": board.id,
                "title": "Changed title",
                "owner_data": {
                    "id": self.owner.id,
                    "email": self.owner.email,
                    "fullname": self.owner.fullname,
                },
                "members_data": [
                    {
                        "id": self.member.id,
                        "email": self.member.email,
                        "fullname": self.member.fullname,
                    }
                ],
            },
        )

    def test_delete_board_as_owner(self):
        """Allow the owner to delete a board."""
        board = Board.objects.create(
            title="Board",
            owner=self.owner,
        )

        response = self.client.delete(self.get_detail_url(board))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Board.objects.filter(id=board.id).exists())

    def test_delete_board_as_member(self):
        """Reject board deletion by a board member."""
        board = Board.objects.create(
            title="Board",
            owner=self.member,
        )
        board.members.add(self.owner)

        response = self.client.delete(self.get_detail_url(board))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Board.objects.filter(id=board.id).exists())

    def test_delete_board_requires_authentication(self):
        """Reject board deletion by unauthenticated users."""
        board = Board.objects.create(
            title="Board",
            owner=self.owner,
        )
        self.client.credentials()

        response = self.client.delete(self.get_detail_url(board))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(Board.objects.filter(id=board.id).exists())

    def test_delete_unknown_board(self):
        """Return not found when deleting an unknown board."""
        url = reverse(
            "boards_app:board-detail",
            kwargs={"board_id": 999999},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

    def test_email_check_returns_user(self):
        """Return user data for an existing email address."""
        response = self.client.get(
            self.email_check_url,
            {"email": self.member.email},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "id": self.member.id,
                "email": self.member.email,
                "fullname": self.member.fullname,
            },
        )

    def test_email_check_requires_email(self):
        """Reject requests without an email query parameter."""
        response = self.client.get(self.email_check_url)

        self.assertEqual(response.status_code, 400)

    def test_email_check_rejects_invalid_email(self):
        """Reject invalid email addresses."""
        response = self.client.get(
            self.email_check_url,
            {"email": "not-an-email"},
        )

        self.assertEqual(response.status_code, 400)

    def test_email_check_returns_not_found(self):
        """Return not found for an unknown email address."""
        response = self.client.get(
            self.email_check_url,
            {"email": "unknown@example.com"},
        )

        self.assertEqual(response.status_code, 404)

    def test_email_check_requires_authentication(self):
        """Reject unauthenticated email checks."""
        self.client.credentials()

        response = self.client.get(
            self.email_check_url,
            {"email": self.member.email},
        )

        self.assertEqual(response.status_code, 401)

    def test_email_check_is_case_insensitive(self):
        """Find users regardless of email letter casing."""
        response = self.client.get(
            self.email_check_url,
            {"email": self.member.email.upper()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.member.id)