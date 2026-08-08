from django.test import TestCase

from users_app.api.serializers import RegistrationSerializer
from users_app.models import User


class RegistrationSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "fullname": "Example Username",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
        }

    def test_valid_registration_data(self):
        serializer = RegistrationSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid())

    def test_create_user(self):
        serializer = RegistrationSerializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, "example@mail.de")
        self.assertTrue(user.check_password("examplePassword"))

    def test_passwords_do_not_match(self):
        self.valid_data["repeated_password"] = "differentPassword"
        serializer = RegistrationSerializer(data=self.valid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("repeated_password", serializer.errors)

    def test_duplicate_email_is_invalid(self):
        User.objects.create_user(
            fullname="Existing User",
            email="example@mail.de",
            password="examplePassword",
        )
        serializer = RegistrationSerializer(data=self.valid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)