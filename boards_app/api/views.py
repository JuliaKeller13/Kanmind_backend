from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Board
from .permissions import HasBoardAccess, IsAuthenticatedBoardUser
from .serializers import (
    BoardDetailSerializer,
    BoardSerializer,
    BoardUpdateSerializer,
)


class BoardViewSet(ModelViewSet):
    """Handle CRUD operations for boards."""

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (
        IsAuthenticatedBoardUser,
        HasBoardAccess,
    )
    lookup_url_kwarg = "board_id"

    def get_queryset(self):
        """Return the appropriate boards for the current action."""
        if self.action == "list":
            user = self.request.user
            return Board.objects.filter(
                Q(owner=user) | Q(members=user)
            ).distinct()
        return Board.objects.all()

    def get_serializer_class(self):
        """Return the serializer required by the current action."""
        if self.action == "retrieve":
            return BoardDetailSerializer
        if self.action == "partial_update":
            return BoardUpdateSerializer
        return BoardSerializer

    def create(self, request, *args, **kwargs):
        """Create a board owned by the authenticated user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save(owner=request.user)

        return Response(
            self.get_serializer(board).data,
            status=status.HTTP_201_CREATED,
        )