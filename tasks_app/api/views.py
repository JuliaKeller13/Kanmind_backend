from rest_framework import status
from rest_framework.exceptions import (
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from boards_app.models import Board

from ..models import Task
from .permissions import (
    HasTaskBoardAccess,
    IsAuthenticatedTaskUser,
    IsTaskCreatorOrBoardOwner,
)
from .serializers import (
    CommentSerializer,
    TaskSerializer,
    TaskUpdateSerializer,
)


class TaskViewSet(ModelViewSet):
    """Handle CRUD operations for tasks."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedTaskUser,)
    lookup_url_kwarg = "task_id"

    def get_serializer_class(self):
        """Return the serializer required by the current action."""
        if self.action == "partial_update":
            return TaskUpdateSerializer
        return TaskSerializer

    def get_permissions(self):
        """Return permissions required for the current action."""
        classes = (IsAuthenticatedTaskUser,)
        if self.action == "partial_update":
            classes += (HasTaskBoardAccess,)
        elif self.action == "destroy":
            classes += (IsTaskCreatorOrBoardOwner,)
        return [permission() for permission in classes]

    def create(self, request, *args, **kwargs):
        """Create a task for a board member."""
        board = self._get_board(request.data.get("board"))
        self._check_board_access(board, request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(created_by=request.user)

        return Response(
            self.get_serializer(task).data,
            status=status.HTTP_201_CREATED,
        )

    def get_object(self):
        """Return the requested task and validate its ID."""
        task_id = self.kwargs[self.lookup_url_kwarg]
        if not str(task_id).isdigit():
            raise ValidationError({"task_id": "Invalid task ID."})

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task not found.") from None

        self.check_object_permissions(self.request, task)
        return task

    @staticmethod
    def _get_board(board_id):
        """Return the requested board when its ID is valid."""
        if board_id is None:
            return None
        try:
            return Board.objects.get(pk=board_id)
        except (Board.DoesNotExist, ValueError, TypeError):
            if str(board_id).isdigit():
                raise NotFound("Board not found.") from None
            return None

    @staticmethod
    def _check_board_access(board, user):
        """Ensure the requesting user is a board member."""
        if board is None:
            return
        if not board.members.filter(id=user.id).exists():
            raise PermissionDenied("You must be a board member.")

class AssignedTasksView(GenericAPIView):
    """Return tasks assigned to the authenticated user."""

    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedTaskUser,)

    def get_queryset(self):
        """Return tasks assigned to the current user."""
        return Task.objects.filter(assignee=self.request.user)

    def get(self, request):
        """Return serialized assigned tasks."""
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True,
        )
        return Response(serializer.data)


class ReviewingTasksView(GenericAPIView):
    """Return tasks reviewed by the authenticated user."""

    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedTaskUser,)

    def get_queryset(self):
        """Return tasks reviewed by the current user."""
        return Task.objects.filter(reviewer=self.request.user)

    def get(self, request):
        """Return serialized reviewing tasks."""
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True,
        )
        return Response(serializer.data)

class TaskCommentListCreateView(GenericAPIView):
    """Create comments belonging to a task."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedTaskUser,
        HasTaskBoardAccess,
    )

    def post(self, request, task_id):
        """Create a comment as an authenticated board member."""
        task = self._get_task(task_id)
        self.check_object_permissions(request, task)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(task=task, author=request.user)

        return Response(
            self.get_serializer(comment).data,
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def _get_task(task_id):
        """Return the requested task or raise not found."""
        try:
            return Task.objects.get(pk=task_id)
        except (Task.DoesNotExist, ValueError, TypeError):
            raise NotFound("Task not found.") from None