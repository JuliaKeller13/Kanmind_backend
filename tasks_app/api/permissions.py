from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAuthenticatedTaskUser(IsAuthenticated):
    """Require authentication for task operations."""


class HasTaskBoardAccess(BasePermission):
    """Allow task access only to members of its board."""

    def has_object_permission(self, request, view, task):
        return task.board.members.filter(id=request.user.id).exists()


class IsTaskCreatorOrBoardOwner(BasePermission):
    """Allow access to the task creator or board owner."""

    def has_object_permission(self, request, view, task):
        user_id = request.user.id
        return (
            task.created_by_id == user_id
            or task.board.owner_id == user_id
        )