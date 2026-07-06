from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


class Comment(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Course",
    )
    content = models.ForeignKey(
        "contents.CourseContent",
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        null=True,
        verbose_name="Content",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="User",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        blank=True,
        null=True,
        verbose_name="Parent Comment",
    )
    text = models.TextField(
        validators=[MinLengthValidator(3)],
        verbose_name="Comment Text",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=["course", "created_at"], name="comment_course_created_idx"),
            models.Index(fields=["content", "created_at"], name="comment_content_created_idx"),
            models.Index(fields=["user", "created_at"], name="comment_user_created_idx"),
            models.Index(fields=["parent"], name="comment_parent_idx"),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.text[:40]}"

    @property
    def comment(self):
        return self.text

    @comment.setter
    def comment(self, value):
        self.text = value

    @property
    def member_id(self):
        class MemberPlaceholder:
            def __init__(self, user):
                self.user_id = user
        return MemberPlaceholder(self.user)


    def clean(self):
        if self.content and self.content.course_id != self.course_id:
            raise ValidationError({"content": "Content must belong to the selected course."})

        if self.course_id and self.user_id and self.course.teacher_id != self.user_id:
            from apps.members.models import Enrollment

            is_enrolled = Enrollment.objects.filter(
                course_id=self.course_id,
                student_id=self.user_id,
                is_active=True,
            ).exists()
            if not is_enrolled:
                raise ValidationError("User must be enrolled before commenting.")
