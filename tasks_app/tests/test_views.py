from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from boards_app.models import Board
from tasks_app.api.serializers import TaskSerializer
from tasks_app.models import Task

User = get_user_model()

class TaskViewSetTest(APITestCase):
    """Test task API endpoints."""

    def setUp(self):
        """Create users, board, and authentication."""
        self.user = self._create_user("member@example.com", "Member")
        self.other_user = self._create_user("other@example.com", "Other")
        self.board = Board.objects.create(title="Project", owner=self.other_user)
        self.board.members.add(self.user)
        self._authenticate(self.user)
        self.url = reverse("tasks_app:task-list")

    @staticmethod
    def _create_user(email, fullname):
        """Create a user for task endpoint tests."""
        return User.objects.create_user(
            email=email,
            password="testpassword",
            fullname=fullname,
        )

    def _authenticate(self, user):
        """Authenticate the API client as the given user."""
        token = Token.objects.get_or_create(user=user)[0]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

    def _valid_data(self):
        """Return valid task creation data."""
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

    def _update_data(self):
        """Return valid task update data."""
        return {
            "title": "Code Review Finished",
            "description": "Finish review and provide feedback",
            "status": "done",
            "priority": "high",
            "assignee_id": self.user.id,
            "reviewer_id": self.user.id,
            "due_date": "2026-08-21",
        }

    def _create_task(self):
        """Create a task belonging to the test board."""
        return Task.objects.create(
            board=self.board,
            created_by=self.user,
            title="Old title",
            description="Old description",
            status=Task.Status.REVIEW,
            priority=Task.Priority.MEDIUM,
            due_date="2026-08-20",
        )

    def _detail_url(self, task):
        """Return the detail URL for a task."""
        return reverse(
            "tasks_app:task-detail",
            kwargs={"task_id": task.id},
        )

    def _user_data(self):
        """Return serialized data for the test member."""
        return {
            "id": self.user.id,
            "email": self.user.email,
            "fullname": self.user.fullname,
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
        self.assertEqual(task.created_by, self.user)

    def test_create_task_response(self):
        """Return the documented task response."""
        response = self.client.post(
            self.url,
            self._valid_data(),
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Code Review")
        self.assertEqual(response.data["assignee"], self._user_data())
        self.assertEqual(response.data["reviewer"], self._user_data())
        self.assertEqual(response.data["comments_count"], 0)

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

    def test_create_task_with_unknown_board(self):
        """Return not found for an unknown board ID."""
        data = self._valid_data()
        data["board"] = 999999
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Task.objects.exists())

    def test_create_task_without_board(self):
        """Reject task creation without a board."""
        data = self._valid_data()
        data.pop("board")
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Task.objects.exists())

    def test_create_task_with_invalid_board_value(self):
        """Reject an invalid board value."""
        data = self._valid_data()
        data["board"] = "abc"
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Task.objects.exists())

    def test_create_task_with_invalid_assignee(self):
        """Reject an assignee who is not a board member."""
        data = self._valid_data()
        data["assignee_id"] = self.other_user.id
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Task.objects.exists())

    def test_update_task(self):
        """Allow a board member to update a task."""
        task = self._create_task()
        response = self.client.patch(
            self._detail_url(task),
            self._update_data(),
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.title, "Code Review Finished")
        self.assertEqual(task.status, Task.Status.DONE)

    def test_update_task_response(self):
        """Return the documented task update response."""
        task = self._create_task()
        response = self.client.patch(
            self._detail_url(task),
            self._update_data(),
            format="json",
        )

        self.assertEqual(response.data["id"], task.id)
        self.assertEqual(response.data["assignee"], self._user_data())
        self.assertEqual(response.data["reviewer"], self._user_data())
        self.assertNotIn("board", response.data)
        self.assertNotIn("comments_count", response.data)

    def test_update_task_partially(self):
        """Update only fields included in the PATCH request."""
        task = self._create_task()
        response = self.client.patch(
            self._detail_url(task),
            {"status": "done"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.DONE)
        self.assertEqual(task.title, "Old title")

    def test_update_task_requires_authentication(self):
        """Reject task updates by unauthenticated users."""
        task = self._create_task()
        self.client.credentials()
        response = self.client.patch(
            self._detail_url(task),
            {"status": "done"},
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_update_task_requires_board_membership(self):
        """Reject updates by users outside the board."""
        task = self._create_task()
        self._authenticate(self.other_user)
        response = self.client.patch(
            self._detail_url(task),
            {"status": "done"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_update_unknown_task(self):
        """Return not found for an unknown task ID."""
        url = reverse(
            "tasks_app:task-detail",
            kwargs={"task_id": 999999},
        )
        response = self.client.patch(
            url,
            {"status": "done"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_update_rejects_board_change(self):
        """Reject attempts to move a task to another board."""
        task = self._create_task()
        data = {"board": 999999}
        response = self.client.patch(
            self._detail_url(task),
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        task.refresh_from_db()
        self.assertEqual(task.board, self.board)

    def test_update_rejects_invalid_status(self):
        """Reject unsupported task status values."""
        task = self._create_task()
        response = self.client.patch(
            self._detail_url(task),
            {"status": "waiting"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_rejects_invalid_assignee(self):
        """Reject assignees outside the task board."""
        task = self._create_task()
        response = self.client.patch(
            self._detail_url(task),
            {"assignee_id": self.other_user.id},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_rejects_invalid_reviewer(self):
        """Reject reviewers outside the task board."""
        task = self._create_task()
        response = self.client.patch(
            self._detail_url(task),
            {"reviewer_id": self.other_user.id},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_delete_task_as_creator(self):
        """Allow the task creator to delete the task."""
        task = self._create_task()

        response = self.client.delete(self._detail_url(task))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
        self.assertIsNone(response.data)

    def test_delete_task_as_board_owner(self):
        """Allow the board owner to delete the task."""
        task = self._create_task()
        self._authenticate(self.other_user)

        response = self.client.delete(self._detail_url(task))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_task_as_board_member(self):
        """Reject deletion by a member who is not creator or owner."""
        member = self._create_user(
            "second-member@example.com",
            "Second Member",
        )
        self.board.members.add(member)
        task = self._create_task()
        self._authenticate(member)

        response = self.client.delete(self._detail_url(task))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_delete_task_requires_authentication(self):
        """Reject task deletion by unauthenticated users."""
        task = self._create_task()
        self.client.credentials()

        response = self.client.delete(self._detail_url(task))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_delete_unknown_task(self):
        """Return not found when deleting an unknown task."""
        url = reverse(
            "tasks_app:task-detail",
            kwargs={"task_id": 999999},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

    def test_delete_task_with_invalid_id(self):
        """Reject an invalid task ID."""
        url = reverse(
            "tasks_app:task-detail",
            kwargs={"task_id": "abc"},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 400)

    def test_assigned_to_me_returns_assigned_tasks(self):
        """Return only tasks assigned to the authenticated user."""
        assigned_task = self._create_task()
        assigned_task.assignee = self.user
        assigned_task.save()

        other_task = self._create_task()
        other_task.assignee = self.other_user
        other_task.save()

        url = reverse("tasks_app:assigned-to-me")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        task_ids = {task["id"] for task in response.data}
        self.assertEqual(task_ids, {assigned_task.id})

    def test_assigned_to_me_requires_authentication(self):
        """Reject unauthenticated access to assigned tasks."""
        self.client.credentials()
        url = reverse("tasks_app:assigned-to-me")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_assigned_to_me_returns_empty_list(self):
        """Return an empty list when no tasks are assigned."""
        url = reverse("tasks_app:assigned-to-me")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_reviewing_returns_review_tasks(self):
        """Return only tasks reviewed by the authenticated user."""
        review_task = self._create_task()
        review_task.reviewer = self.user
        review_task.save()

        other_task = self._create_task()
        other_task.reviewer = self.other_user
        other_task.save()

        url = reverse("tasks_app:reviewing")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        task_ids = {task["id"] for task in response.data}
        self.assertEqual(task_ids, {review_task.id})

    def test_reviewing_requires_authentication(self):
        """Reject unauthenticated access to reviewing tasks."""
        self.client.credentials()
        url = reverse("tasks_app:reviewing")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_reviewing_returns_empty_list(self):
        """Return an empty list when no tasks are under review."""
        url = reverse("tasks_app:reviewing")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_create_comment(self):
        """Create a comment as a board member."""
        task = self._create_task()
        url = reverse(
            "tasks_app:task-comments",
            kwargs={"task_id": task.id},
        )

        response = self.client.post(
            url,
            {"content": "New comment"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["content"], "New comment")
        self.assertEqual(response.data["author"], self.user.fullname)

    def test_create_comment_sets_author_and_task(self):
        """Store the authenticated user and task on the comment."""
        task = self._create_task()
        url = reverse(
            "tasks_app:task-comments",
            kwargs={"task_id": task.id},
        )

        self.client.post(
            url,
            {"content": "New comment"},
            format="json",
        )

        comment = task.comments.get()
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.task, task)

    def test_create_comment_rejects_empty_content(self):
        """Reject comments with empty content."""
        task = self._create_task()
        url = reverse(
            "tasks_app:task-comments",
            kwargs={"task_id": task.id},
        )

        response = self.client.post(
            url,
            {"content": ""},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_create_comment_requires_authentication(self):
        """Reject comment creation by unauthenticated users."""
        task = self._create_task()
        self.client.credentials()
        url = reverse(
            "tasks_app:task-comments",
            kwargs={"task_id": task.id},
        )

        response = self.client.post(
            url,
            {"content": "New comment"},
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_create_comment_requires_board_membership(self):
        """Reject comment creation by non-board members."""
        task = self._create_task()
        self._authenticate(self.other_user)
        url = reverse(
            "tasks_app:task-comments",
            kwargs={"task_id": task.id},
        )

        response = self.client.post(
            url,
            {"content": "New comment"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_create_comment_for_unknown_task(self):
        """Return not found for an unknown task."""
        url = reverse(
            "tasks_app:task-comments",
            kwargs={"task_id": 999999},
        )

        response = self.client.post(
            url,
            {"content": "New comment"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_comment_increases_comments_count(self):
        """Increase the serialized task comment count."""
        task = self._create_task()
        url = reverse(
            "tasks_app:task-comments",
            kwargs={"task_id": task.id},
        )

        self.client.post(
            url,
            {"content": "New comment"},
            format="json",
        )

        serializer = TaskSerializer(task)

        self.assertEqual(serializer.data["comments_count"], 1)