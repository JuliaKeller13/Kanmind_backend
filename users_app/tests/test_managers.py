from django.test import TestCase

from users_app.models import User


class UserManagerTest(TestCase):
    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password="examplePassword",
            )

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.de",
            password="examplePassword",
            fullname="Admin User",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("examplePassword"))

    def test_superuser_requires_is_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.de",
                password="examplePassword",
                fullname="Admin User",
                is_staff=False,
            )

    def test_superuser_requires_is_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.de",
                password="examplePassword",
                fullname="Admin User",
                is_superuser=False,
            )