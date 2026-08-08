from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RegistrationSerializer


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)

        return Response(
            self._response_data(user, token.key),
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def _response_data(user, token):
        return {
            "token": token,
            "fullname": user.fullname,
            "email": user.email,
            "user_id": user.id,
        }