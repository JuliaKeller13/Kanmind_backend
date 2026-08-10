from django.test import TestCase

from users_app.models import User


class UserModelTest(TestCase):
    def test_user_string_representation(self):
        user = User.objects.create_user(
            fullname="Example Username",
            email="example@mail.de",
            password="examplePassword",
        )

        self.assertEqual(str(user), "example@mail.de")