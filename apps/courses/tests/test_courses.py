from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from ninja_simple_jwt.jwt.token_operations import get_access_token_for_user

from apps.courses.models import Course

User = get_user_model()


class CourseTests(TestCase):
    def setUp(self):
        # Create users
        self.teacher = User.objects.create_user(
            username="teacher01",
            email="teacher01@example.com",
            password="SecurePassword123",
            role="teacher",
        )
        self.student = User.objects.create_user(
            username="student01",
            email="student01@example.com",
            password="SecurePassword123",
            role="student",
        )
        
        # Create courses
        self.course1 = Course.objects.create(
            title="Django Advanced Course",
            slug="django-advanced-course",
            teacher=self.teacher,
            category="Backend",
            price=Decimal("150000.00"),
            status=Course.Status.PUBLISHED,
        )
        self.course2 = Course.objects.create(
            title="Intro to Python programming",
            slug="intro-to-python-programming",
            teacher=self.teacher,
            category="Programming",
            price=Decimal("0.00"),
            status=Course.Status.PUBLISHED,
        )

        self.list_url = reverse("smart_lms_api:list_courses")
        self.create_url = reverse("smart_lms_api:create_course")

        # Generate tokens
        self.teacher_token, _ = get_access_token_for_user(self.teacher)
        self.student_token, _ = get_access_token_for_user(self.student)

    def test_list_courses_anonymous_success(self):
        # Anonymous users can access courses
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 2)

    def test_course_filtering_by_search(self):
        # Filter search="python"
        response = self.client.get(self.list_url, {"search": "python"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["title"], "Intro to Python programming")

    def test_course_filtering_by_price_limit(self):
        # Filter price_gte=100000
        response = self.client.get(self.list_url, {"price_gte": 100000})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["title"], "Django Advanced Course")

    def test_course_pagination_limit(self):
        # Create additional courses to test page size of 5
        for i in range(10):
            Course.objects.create(
                title=f"Sample Course {i}",
                slug=f"sample-course-{i}",
                teacher=self.teacher,
                category="General",
                price=Decimal("10000.00"),
                status=Course.Status.PUBLISHED,
            )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["page_size"], 5)  # verified default is 5
        self.assertEqual(len(data["results"]), 5)

    def test_create_course_teacher_allowed(self):
        payload = {
            "title": "New Web Development Course",
            "category": "Frontend",
            "price": "200000.00",
            "description": "Learn HTML, CSS and JS",
            "status": "draft",
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Course.objects.filter(title="New Web Development Course").exists())

    def test_create_course_student_forbidden(self):
        payload = {
            "title": "Student Unauthorized Course",
            "category": "Frontend",
            "price": "200000.00",
            "description": "Learn HTML",
            "status": "draft",
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 403)
