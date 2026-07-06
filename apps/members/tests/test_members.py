from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from ninja_simple_jwt.jwt.token_operations import get_access_token_for_user

from apps.courses.models import Course
from apps.members.models import CourseMember, Enrollment

User = get_user_model()


class EnrollmentTests(TestCase):
    def setUp(self):
        # Create users
        self.teacher = User.objects.create_user(
            username="teacher_m01",
            email="teacher_m01@example.com",
            password="SecurePassword123",
            role="teacher",
        )
        self.student = User.objects.create_user(
            username="student_m01",
            email="student_m01@example.com",
            password="SecurePassword123",
            role="student",
        )
        self.student2 = User.objects.create_user(
            username="student_m02",
            email="student_m02@example.com",
            password="SecurePassword123",
            role="student",
        )

        # Create course
        self.course = Course.objects.create(
            title="Enrollment Test Course",
            slug="enrollment-test-course",
            teacher=self.teacher,
            category="Backend",
            price=Decimal("50000.00"),
            status=Course.Status.PUBLISHED,
            description="Course for enrollment tests",
        )

        # Generate tokens
        self.teacher_token, _ = get_access_token_for_user(self.teacher)
        self.student_token, _ = get_access_token_for_user(self.student)
        self.student2_token, _ = get_access_token_for_user(self.student2)

        self.enroll_url = reverse("smart_lms_api:enroll_course", args=[self.course.id])
        self.leave_url = reverse("smart_lms_api:leave_course", args=[self.course.id])
        self.list_members_url = reverse("smart_lms_api:list_members", args=[self.course.id])

    def test_student_can_enroll(self):
        """Student can successfully enroll in a course."""
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.post(self.enroll_url, **headers)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["course_id"], self.course.id)
        self.assertTrue(data["is_active"])
        # Verify enrollment and CourseMember created
        self.assertTrue(Enrollment.objects.filter(course=self.course, student=self.student, is_active=True).exists())
        self.assertTrue(CourseMember.objects.filter(course=self.course, user=self.student).exists())

    def test_teacher_cannot_enroll(self):
        """Teacher cannot enroll as a student."""
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.post(self.enroll_url, **headers)
        self.assertEqual(response.status_code, 403)

    def test_duplicate_enrollment_rejected(self):
        """Student cannot enroll twice in the same course."""
        Enrollment.objects.create(course=self.course, student=self.student, is_active=True)
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.post(self.enroll_url, **headers)
        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_enroll_rejected(self):
        """Unauthenticated user cannot enroll."""
        response = self.client.post(self.enroll_url)
        self.assertEqual(response.status_code, 401)

    def test_student_can_leave_course(self):
        """Enrolled student can leave a course."""
        Enrollment.objects.create(course=self.course, student=self.student, is_active=True)
        CourseMember.objects.create(course=self.course, user=self.student, role=CourseMember.Role.STUDENT)
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.post(self.leave_url, **headers)
        self.assertEqual(response.status_code, 200)
        # Enrollment marked inactive
        enrollment = Enrollment.objects.get(course=self.course, student=self.student)
        self.assertFalse(enrollment.is_active)

    def test_leave_when_not_enrolled_returns_404(self):
        """Leaving a course without active enrollment returns 404."""
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.post(self.leave_url, **headers)
        self.assertEqual(response.status_code, 404)

    def test_teacher_can_list_members(self):
        """Teacher can list course members."""
        Enrollment.objects.create(course=self.course, student=self.student, is_active=True)
        CourseMember.objects.create(course=self.course, user=self.student, role=CourseMember.Role.STUDENT)
        CourseMember.objects.create(course=self.course, user=self.teacher, role=CourseMember.Role.TEACHER)
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.get(self.list_members_url, **headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 1)

    def test_student_cannot_list_members(self):
        """Student cannot list members (teacher-only)."""
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.get(self.list_members_url, **headers)
        self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_view_other_course_members(self):
        """Teacher cannot view members for another teacher's course."""
        other_teacher = User.objects.create_user(
            username="other_teacher_m01",
            email="other_teacher_m01@example.com",
            password="SecurePassword123",
            role="teacher",
        )
        other_token, _ = get_access_token_for_user(other_teacher)
        headers = {"HTTP_AUTHORIZATION": f"Bearer {other_token}"}
        response = self.client.get(self.list_members_url, **headers)
        self.assertEqual(response.status_code, 403)
