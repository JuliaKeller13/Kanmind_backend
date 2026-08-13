from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Board
from .permissions import (
    HasBoardAccess,
    IsAuthenticatedBoardUser,
    IsBoardOwner,
)
from .serializers import (
    BoardDetailSerializer,
    BoardMemberSerializer,
    BoardSerializer,
    BoardUpdateSerializer,
    EmailCheckSerializer,
)

User = get_user_model()


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

    def get_permissions(self):
        """Return permissions required for the current action."""
        if self.action == "destroy":
            classes = (IsAuthenticatedBoardUser, IsBoardOwner)
        elif self.action in ("retrieve", "partial_update"):
            classes = (IsAuthenticatedBoardUser, HasBoardAccess)
        else:
            classes = (IsAuthenticatedBoardUser,)
        return [permission() for permission in classes]

class EmailCheckView(GenericAPIView):
    """Return a registered user matching an email address."""

    serializer_class = EmailCheckSerializer
    permission_classes = (IsAuthenticatedBoardUser,)

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            raise NotFound("Email not found.")

        return Response(BoardMemberSerializer(user).data)