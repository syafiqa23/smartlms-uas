from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.register_url = reverse("smart_lms_api:register")
        self.login_url = reverse("smart_lms_api:login")
        self.refresh_url = reverse("smart_lms_api:refresh_token")

    def test_register_student_success(self):
        payload = {
            "username": "student01",
            "email": "student01@example.com",
            "password": "SecurePassword123",
            "first_name": "Budi",
            "last_name": "Santoso",
            "role": "student",
        }
        response = self.client.post(
            self.register_url, payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["username"], "student01")
        self.assertEqual(data["email"], "student01@example.com")
        self.assertEqual(data["role"], "student")
        self.assertTrue(User.objects.filter(username="student01").exists())

    def test_register_password_validation_fails(self):
        # Password must contain at least one number — Ninja/Pydantic returns 422 for schema-level validation
        payload = {
            "username": "student02",
            "email": "student02@example.com",
            "password": "NoNumbersPassword",
            "role": "student",
        }
        response = self.client.post(
            self.register_url, payload, content_type="application/json"
        )
        # Django Ninja returns 422 for Pydantic field_validator errors
        self.assertEqual(response.status_code, 422)

    def test_login_success(self):
        user = User.objects.create_user(
            username="student10",
            email="student10@example.com",
            password="SecurePassword123",
            role="student",
        )
        payload = {"username": "student10", "password": "SecurePassword123"}
        response = self.client.post(
            self.login_url, payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)
        self.assertEqual(data["token_type"], "Bearer")

    def test_login_invalid_credentials(self):
        payload = {"username": "nonexistent", "password": "WrongPassword123"}
        response = self.client.post(
            self.login_url, payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_jwt_token_refresh(self):
        user = User.objects.create_user(
            username="student11",
            email="student11@example.com",
            password="SecurePassword123",
            role="student",
        )
        # Login to get refresh token
        login_payload = {"username": "student11", "password": "SecurePassword123"}
        login_response = self.client.post(
            self.login_url, login_payload, content_type="application/json"
        )
        refresh_token = login_response.json()["refresh"]

        # Call refresh endpoint
        refresh_payload = {"refresh": refresh_token}
        response = self.client.post(
            self.refresh_url, refresh_payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
