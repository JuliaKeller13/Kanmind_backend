from django.contrib.auth import get_user_model
from django.test import TestCase

from boards_app.api.serializers import BoardSerializer
from boards_app.models import Board

User = get_user_model()


class BoardSerializerTest(TestCase):
    """Test board serialization and creation."""

    def setUp(self):
        """Create users required for serializer tests."""
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

    def test_create_board_with_members(self):
        """Create a board with valid member IDs."""
        data = {
            "title": "New Project",
            "members": [self.member.id],
        }

        serializer = BoardSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        board = serializer.save(owner=self.owner)

        self.assertEqual(board.title, "New Project")
        self.assertEqual(board.owner, self.owner)
        self.assertIn(self.member, board.members.all())

    def test_board_response_data(self):
        """Return the documented board response fields."""
        board = Board.objects.create(
            title="New Project",
            owner=self.owner,
        )
        board.members.add(self.member)

        serializer = BoardSerializer(board)

        self.assertEqual(
            serializer.data,
            {
                "id": board.id,
                "title": "New Project",
                "member_count": 1,
                "ticket_count": 0,
                "tasks_to_do_count": 0,
                "tasks_high_prio_count": 0,
                "owner_id": self.owner.id,
            },
        )