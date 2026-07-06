from django.conf import settings
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models


class Course(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(
        max_length=180,
        validators=[MinLengthValidator(5)],
        db_index=True,
        verbose_name="Course Title",
    )
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Teacher",
    )
    thumbnail = models.ImageField(
        upload_to="course_thumbnails/",
        blank=True,
        null=True,
        verbose_name="Thumbnail",
    )
    category = models.CharField(max_length=80, db_index=True, verbose_name="Category")
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        db_index=True,
        verbose_name="Price",
    )
    description = models.TextField(verbose_name="Description")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["-created_at", "title"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        indexes = [
            models.Index(fields=["title"], name="course_title_idx"),
            models.Index(fields=["category", "status"], name="course_category_status_idx"),
            models.Index(fields=["teacher", "status"], name="course_teacher_status_idx"),
            models.Index(fields=["price"], name="course_price_idx"),
            models.Index(fields=["created_at"], name="course_created_idx"),
        ]

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title

    @name.setter
    def name(self, value):
        self.title = value

