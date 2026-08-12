from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Board
from .permissions import IsAuthenticatedBoardUser
from .serializers import BoardSerializer


class BoardViewSet(ModelViewSet):
    """Handle CRUD operations for boards."""

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (IsAuthenticatedBoardUser,)
    http_method_names = ("post",)

    def create(self, request, *args, **kwargs):
        """Create a board owned by the authenticated user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save(owner=request.user)

        return Response(
            self.get_serializer(board).data,
            status=status.HTTP_201_CREATED,
        )