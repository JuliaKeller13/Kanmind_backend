from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .responses import build_auth_response
from .serializers import LoginSerializer, RegistrationSerializer


class RegistrationView(GenericAPIView):
    """Register a new user and return an authentication token."""

    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """Create a user account and return authentication data."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)

        return Response(
            build_auth_response(user, token.key),
            status=status.HTTP_201_CREATED,
        )


class LoginView(GenericAPIView):
    """Authenticate a user and return an authentication token."""

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """Authenticate credentials and return authentication data."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            build_auth_response(user, token.key),
            status=status.HTTP_200_OK,
        )