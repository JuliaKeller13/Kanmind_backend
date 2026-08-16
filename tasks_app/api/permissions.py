from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAuthenticatedTaskUser(IsAuthenticated):
    """Require authentication for task operations."""


class HasTaskBoardAccess(BasePermission):
    """Allow task access only to members of its board."""

    def has_object_permission(self, request, view, task):
        return task.board.members.filter(id=request.user.id).exists()