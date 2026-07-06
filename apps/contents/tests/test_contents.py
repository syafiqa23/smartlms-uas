from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from ninja_simple_jwt.jwt.token_operations import get_access_token_for_user

from apps.contents.models import CourseContent
from apps.courses.models import Course

User = get_user_model()


class CourseContentTests(TestCase):
    def setUp(self):
        # Create users
        self.teacher = User.objects.create_user(
            username="teacher_cn01",
            email="teacher_cn01@example.com",
            password="SecurePassword123",
            role="teacher",
        )
        self.teacher2 = User.objects.create_user(
            username="teacher_cn02",
            email="teacher_cn02@example.com",
            password="SecurePassword123",
            role="teacher",
        )
        self.student = User.objects.create_user(
            username="student_cn01",
            email="student_cn01@example.com",
            password="SecurePassword123",
            role="student",
        )

        # Create course
        self.course = Course.objects.create(
            title="Content Test Course",
            slug="content-test-course",
            teacher=self.teacher,
            category="Backend",
            price=Decimal("0.00"),
            status=Course.Status.PUBLISHED,
            description="Course for content tests",
        )

        # Create a content item
        self.content = CourseContent.objects.create(
            course=self.course,
            title="Lesson 1 - Introduction",
            description="First lesson",
            order=1,
        )

        # Generate tokens
        self.teacher_token, _ = get_access_token_for_user(self.teacher)
        self.teacher2_token, _ = get_access_token_for_user(self.teacher2)
        self.student_token, _ = get_access_token_for_user(self.student)

        self.list_url = reverse("smart_lms_api:list_contents")
        self.create_url = reverse("smart_lms_api:create_content")
        self.detail_url = reverse("smart_lms_api:get_content", args=[self.content.id])
        self.update_url = reverse("smart_lms_api:update_content", args=[self.content.id])
        self.delete_url = reverse("smart_lms_api:delete_content", args=[self.content.id])

    def test_list_contents_requires_auth(self):
        """Listing contents requires authentication."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 401)

    def test_list_contents_for_course(self):
        """Teacher can list contents for a course."""
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.get(self.list_url, {"course_id": self.course.id}, **headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Lesson 1 - Introduction")

    def test_get_content_detail(self):
        """Authenticated user can retrieve content detail."""
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.get(self.detail_url, **headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], self.content.id)
        self.assertEqual(data["title"], "Lesson 1 - Introduction")

    def test_create_content_teacher_owner_allowed(self):
        """Course owner teacher can create content."""
        payload = {
            "course_id": self.course.id,
            "title": "Lesson 2 - ORM Basics",
            "description": "Learn ORM",
            "order": 2,
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "Lesson 2 - ORM Basics")

    def test_create_content_other_teacher_forbidden(self):
        """Another teacher cannot create content for someone else's course."""
        payload = {
            "course_id": self.course.id,
            "title": "Unauthorized Lesson",
            "description": "Should not work",
            "order": 3,
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher2_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 403)

    def test_create_content_student_forbidden(self):
        """Student cannot create content."""
        payload = {
            "course_id": self.course.id,
            "title": "Student Unauthorized Lesson",
            "description": "Should not work",
            "order": 4,
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 403)

    def test_update_content_teacher_owner_allowed(self):
        """Course owner teacher can update content."""
        payload = {"title": "Lesson 1 - Updated Introduction"}
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.patch(
            self.update_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Lesson 1 - Updated Introduction")

    def test_delete_content_teacher_owner_allowed(self):
        """Course owner teacher can delete content."""
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.delete(self.delete_url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CourseContent.objects.filter(id=self.content.id).exists())

    def test_delete_content_other_teacher_forbidden(self):
        """Another teacher cannot delete content from someone else's course."""
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher2_token}"}
        response = self.client.delete(self.delete_url, **headers)
        self.assertEqual(response.status_code, 403)

    def test_duplicate_order_rejected(self):
        """Creating content with duplicate order in same course should fail."""
        payload = {
            "course_id": self.course.id,
            "title": "Duplicate Order Lesson",
            "description": "Duplicate order",
            "order": 1,  # Already exists
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 400)
