from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory

from users_app.api.views import RegistrationView
from users_app.models import User


class RegistrationViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = RegistrationView.as_view()
        self.valid_data = {
            "fullname": "Example Username",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
        }

    def _post_registration(self, data):
        request = self.factory.post(
            "/api/registration/",
            data,
            format="json",
        )
        return self.view(request)

    def test_registration_returns_expected_response(self):
        response = self._post_registration(self.valid_data)
        user = User.objects.get(email="example@mail.de")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["fullname"], user.fullname)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["user_id"], user.id)
        self.assertIn("token", response.data)

    def test_registration_creates_token(self):
        response = self._post_registration(self.valid_data)
        user = User.objects.get(email="example@mail.de")

        token_exists = Token.objects.filter(
            user=user,
            key=response.data["token"],
        ).exists()

        self.assertTrue(token_exists)

    def test_registration_rejects_different_passwords(self):
        data = self.valid_data.copy()
        data["repeated_password"] = "differentPassword"

        response = self._post_registration(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("repeated_password", response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_registration_rejects_duplicate_email(self):
        User.objects.create_user(
            fullname="Existing User",
            email="example@mail.de",
            password="examplePassword",
        )

        response = self._post_registration(self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_registration_endpoint(self):
        url = reverse("users_app:registration")

        response = self.client.post(url, self.valid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertIn("token", response.data)