from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAuthenticatedBoardUser(IsAuthenticated):
    """Require authentication for board operations."""


class HasBoardAccess(BasePermission):
    """Allow access to board owners and members."""

    def has_object_permission(self, request, view, board):
        return (
            board.owner_id == request.user.id
            or board.members.filter(id=request.user.id).exists()
        )

class IsBoardOwner(BasePermission):
    """Allow access only to the board owner."""

    def has_object_permission(self, request, view, board):
        return board.owner_id == request.user.id