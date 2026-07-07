import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from apps.courses.models import Course
from apps.members.models import CourseMember

User = get_user_model()


class Command(BaseCommand):
    help = "Imports courses from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")
        parser.add_argument(
            "--teacher-username",
            type=str,
            help="Username of the teacher to assign to imported courses (optional)",
        )

    def handle(self, *args, **options):
        csv_file_path = options["csv_file"]
        teacher_username = options.get("teacher_username")
        teacher = None

        if teacher_username:
            try:
                teacher = User.objects.get(username=teacher_username)
                if teacher.role not in [User.Role.TEACHER, User.Role.ADMIN]:
                    self.stdout.write(
                        self.style.ERROR(
                            f"User {teacher_username} is not a teacher or admin"
                        )
                    )
                    return
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"User {teacher_username} does not exist")
                )
                return

        self.stdout.write(self.style.SUCCESS(f"Importing courses from {csv_file_path}"))

        imported_count = 0
        skipped_count = 0

        try:
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    title = row.get("title")
                    if not title:
                        self.stdout.write(
                            self.style.WARNING("Skipping row: title is required")
                        )
                        skipped_count += 1
                        continue

                    # Check if course with same title already exists
                    if Course.objects.filter(title=title).exists():
                        self.stdout.write(
                            self.style.WARNING(f"Skipping course: {title} (already exists)")
                        )
                        skipped_count += 1
                        continue

                    # Get or create teacher if not provided
                    course_teacher = teacher
                    if not course_teacher:
                        # Try to use teacher_username from CSV, or default to first admin/teacher
                        csv_teacher_username = row.get("teacher_username")
                        if csv_teacher_username:
                            try:
                                course_teacher = User.objects.get(username=csv_teacher_username)
                            except User.DoesNotExist:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"Teacher {csv_teacher_username} not found, using default teacher"
                                    )
                                )
                        # Fallback to first available teacher/admin
                        if not course_teacher:
                            course_teacher = User.objects.filter(
                                role__in=[User.Role.TEACHER, User.Role.ADMIN]
                            ).first()
                            if not course_teacher:
                                self.stdout.write(
                                    self.style.ERROR("No teacher/admin users found to assign courses")
                                )
                                return

                    category = row.get("category", "Uncategorized")
                    price = float(row.get("price", 0))
                    description = row.get("description", "")
                    status = row.get("status", Course.Status.DRAFT)

                    # Ensure valid status
                    valid_statuses = [choice[0] for choice in Course.Status.choices]
                    if status not in valid_statuses:
                        status = Course.Status.DRAFT

                    course = Course.objects.create(
                        title=title,
                        slug=slugify(title),
                        teacher=course_teacher,
                        category=category,
                        price=price,
                        description=description,
                        status=status,
                    )

                    # Add teacher as course member
                    CourseMember.objects.get_or_create(
                        course=course,
                        user=course_teacher,
                        defaults={"role": CourseMember.Role.TEACHER},
                    )

                    self.stdout.write(f"Imported course: {title}")
                    imported_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Import completed! Imported: {imported_count}, Skipped: {skipped_count}"
                )
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing courses: {str(e)}"))
