from django.conf import settings
from django.db import models


class CourseMember(models.Model):
    class Role(models.TextChoices):
        TEACHER = "teacher", "Teacher"
        STUDENT = "student", "Student"

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Course",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_memberships",
        verbose_name="User",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        db_index=True,
        verbose_name="Member Role",
    )
    joined_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Joined At")

    class Meta:
        ordering = ["-joined_at"]
        verbose_name = "Course Member"
        verbose_name_plural = "Course Members"
        constraints = [
            models.UniqueConstraint(fields=["course", "user"], name="unique_course_member"),
        ]
        indexes = [
            models.Index(fields=["course", "role"], name="member_course_role_idx"),
            models.Index(fields=["user", "role"], name="member_user_role_idx"),
            models.Index(fields=["joined_at"], name="member_joined_idx"),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.role})"

    @property
    def course_id(self):
        return self.course



class Enrollment(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Course",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Student",
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Enrolled At")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Is Active")

    class Meta:
        ordering = ["-enrolled_at"]
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        constraints = [
            models.UniqueConstraint(fields=["course", "student"], name="unique_course_enrollment"),
        ]
        indexes = [
            models.Index(fields=["course", "is_active"], name="enroll_course_active_idx"),
            models.Index(fields=["student", "is_active"], name="enroll_student_active_idx"),
            models.Index(fields=["enrolled_at"], name="enroll_date_idx"),
        ]

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

    @property
    def course_id(self):
        return self.course

