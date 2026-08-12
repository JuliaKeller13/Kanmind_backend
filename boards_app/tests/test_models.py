from django.contrib.auth import get_user_model
from django.test import TestCase

from boards_app.models import Board

User = get_user_model()


class BoardModelTest(TestCase):
    """Test board model behavior."""

    def test_string_representation(self):
        """Return the board title as its string representation."""
        owner = User.objects.create_user(
            email="owner@example.com",
            password="testpassword",
            fullname="Board Owner",
        )
        board = Board.objects.create(
            title="New Project",
            owner=owner,
        )

        self.assertEqual(str(board), "New Project")