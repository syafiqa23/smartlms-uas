from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models


class CourseContent(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="contents",
        verbose_name="Course",
    )
    title = models.CharField(
        max_length=180,
        validators=[MinLengthValidator(5)],
        verbose_name="Content Title",
    )
    video_url = models.URLField(blank=True, verbose_name="Video URL")
    attachment = models.FileField(
        upload_to="attachments/",
        blank=True,
        null=True,
        verbose_name="Attachment",
    )
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Order",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["course", "order", "id"]
        verbose_name = "Course Content"
        verbose_name_plural = "Course Contents"
        constraints = [
            models.UniqueConstraint(fields=["course", "order"], name="unique_content_order_per_course"),
        ]
        indexes = [
            models.Index(fields=["course", "order"], name="content_course_order_idx"),
            models.Index(fields=["created_at"], name="content_created_idx"),
        ]

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    @property
    def name(self):
        return self.title

    @name.setter
    def name(self, value):
        self.title = value

    @property
    def file_attachment(self):
        return self.attachment

    @property
    def course_id(self):
        return self.course

