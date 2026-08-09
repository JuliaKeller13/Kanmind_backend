from django.test import TestCase
from rest_framework.authtoken.models import Token

from users_app.api.responses import build_auth_response
from users_app.models import User


class AuthResponseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            fullname="Example Username",
            email="example@mail.de",
            password="examplePassword",
        )
        self.token = Token.objects.create(user=self.user)

    def test_build_auth_response(self):
        response_data = build_auth_response(
            self.user,
            self.token.key,
        )

        self.assertEqual(response_data["token"], self.token.key)
        self.assertEqual(response_data["fullname"], self.user.fullname)
        self.assertEqual(response_data["email"], self.user.email)
        self.assertEqual(response_data["user_id"], self.user.id)