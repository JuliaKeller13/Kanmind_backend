from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from boards_app.models import Board

from ..models import Task
from .permissions import HasTaskBoardAccess, IsAuthenticatedTaskUser
from .serializers import TaskSerializer, TaskUpdateSerializer


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
        return [permission() for permission in classes]

    def create(self, request, *args, **kwargs):
        """Create a task for a board member."""
        board = self._get_board(request.data.get("board"))
        self._check_board_access(board, request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()

        return Response(
            self.get_serializer(task).data,
            status=status.HTTP_201_CREATED,
        )

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