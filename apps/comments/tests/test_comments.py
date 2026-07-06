from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from ninja_simple_jwt.jwt.token_operations import get_access_token_for_user

from apps.comments.models import Comment
from apps.contents.models import CourseContent
from apps.courses.models import Course
from apps.members.models import Enrollment

User = get_user_model()


class CommentTests(TestCase):
    def setUp(self):
        # Create users
        self.teacher = User.objects.create_user(
            username="teacher_c01",
            email="teacher_c01@example.com",
            password="SecurePassword123",
            role="teacher",
        )
        self.student = User.objects.create_user(
            username="student_c01",
            email="student_c01@example.com",
            password="SecurePassword123",
            role="student",
        )
        self.student2 = User.objects.create_user(
            username="student_c02",
            email="student_c02@example.com",
            password="SecurePassword123",
            role="student",
        )

        # Create course
        self.course = Course.objects.create(
            title="Django Advanced Course",
            slug="django-advanced-comment-test",
            teacher=self.teacher,
            category="Backend",
            price=Decimal("0.00"),
            status=Course.Status.PUBLISHED,
            description="Test course for comments",
        )

        # Create content
        self.content = CourseContent.objects.create(
            course=self.course,
            title="Lesson 1 - Intro",
            description="Intro content",
            order=1,
        )

        # Enroll student
        Enrollment.objects.create(course=self.course, student=self.student, is_active=True)

        # Generate tokens
        self.teacher_token, _ = get_access_token_for_user(self.teacher)
        self.student_token, _ = get_access_token_for_user(self.student)
        self.student2_token, _ = get_access_token_for_user(self.student2)

        self.list_url = reverse("smart_lms_api:list_comments")
        self.create_url = reverse("smart_lms_api:create_comment")

    def test_list_comments_requires_auth(self):
        """Listing comments requires authentication."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 401)

    def test_list_comments_authenticated(self):
        """Authenticated user can list comments."""
        Comment.objects.create(
            course=self.course,
            user=self.teacher,
            text="Teacher comment here",
        )
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.get(
            self.list_url, {"course_id": self.course.id}, **headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)

    def test_create_comment_teacher_can_comment(self):
        """Teacher can comment on their own course without enrollment."""
        payload = {
            "course_id": self.course.id,
            "text": "Great discussion going on!",
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.teacher_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["text"], "Great discussion going on!")

    def test_create_comment_enrolled_student_allowed(self):
        """Enrolled student can post a comment."""
        payload = {
            "course_id": self.course.id,
            "text": "Great course material!",
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["text"], "Great course material!")
        self.assertEqual(data["username"], "student_c01")

    def test_create_comment_non_enrolled_student_forbidden(self):
        """Non-enrolled student cannot post a comment."""
        payload = {
            "course_id": self.course.id,
            "text": "I should not be allowed here",
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student2_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 403)

    def test_create_nested_reply(self):
        """Enrolled student can reply to an existing comment."""
        parent = Comment.objects.create(
            course=self.course,
            user=self.teacher,
            text="Top-level teacher comment",
        )
        payload = {
            "course_id": self.course.id,
            "parent_id": parent.id,
            "text": "Reply from enrolled student",
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["parent_id"], parent.id)

    def test_update_own_comment_success(self):
        """User can update their own comment."""
        comment = Comment.objects.create(
            course=self.course,
            user=self.student,
            text="Original comment text",
        )
        Enrollment.objects.filter(course=self.course, student=self.student).update(is_active=True)
        update_url = reverse("smart_lms_api:update_comment", args=[comment.id])
        payload = {"text": "Updated comment text"}
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.patch(
            update_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], "Updated comment text")

    def test_update_other_user_comment_forbidden(self):
        """User cannot update another user's comment."""
        comment = Comment.objects.create(
            course=self.course,
            user=self.teacher,
            text="Teacher's original comment",
        )
        update_url = reverse("smart_lms_api:update_comment", args=[comment.id])
        payload = {"text": "Trying to edit teacher comment"}
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.patch(
            update_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_own_comment_success(self):
        """User can delete their own comment."""
        comment = Comment.objects.create(
            course=self.course,
            user=self.student,
            text="Comment to delete",
        )
        delete_url = reverse("smart_lms_api:delete_comment", args=[comment.id])
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.delete(delete_url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())

    def test_delete_other_user_comment_forbidden(self):
        """User cannot delete another user's comment."""
        comment = Comment.objects.create(
            course=self.course,
            user=self.teacher,
            text="Teacher's comment to protect",
        )
        delete_url = reverse("smart_lms_api:delete_comment", args=[comment.id])
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.delete(delete_url, **headers)
        self.assertEqual(response.status_code, 403)

    def test_comment_text_too_short_fails(self):
        """Comment text shorter than 3 characters should fail validation."""
        payload = {
            "course_id": self.course.id,
            "text": "Hi",
        }
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.student_token}"}
        response = self.client.post(
            self.create_url, payload, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 422)
