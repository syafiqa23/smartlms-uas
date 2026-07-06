import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from apps.courses.models import Course
from apps.contents.models import CourseContent
from apps.comments.models import Comment
from apps.members.models import CourseMember, Enrollment

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with dummy data for Smart LMS"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting data seeding..."))

        # Clear existing data
        self.stdout.write("Clearing existing data...")
        Comment.objects.all().delete()
        CourseContent.objects.all().delete()
        CourseMember.objects.all().delete()
        Enrollment.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()

        # Create Admin
        self.stdout.write("Creating admin user...")
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@smartlms.com",
            password="admin123",
            role=User.Role.ADMIN,
            first_name="Smart",
            last_name="Admin",
        )

        # Create Teachers
        self.stdout.write("Creating teacher users...")
        teachers = []
        teacher_data = [
            ("budi_guru", "budi@smartlms.com", "Budi", "Santoso"),
            ("siti_guru", "siti@smartlms.com", "Siti", "Nurhaliza"),
        ]
        for username, email, first, last in teacher_data:
            teacher = User.objects.create_user(
                username=username,
                email=email,
                password="teacher123",
                role=User.Role.TEACHER,
                first_name=first,
                last_name=last,
            )
            teachers.append(teacher)

        # Create Students
        self.stdout.write("Creating student users...")
        students = []
        student_data = [
            ("andi_mhs", "andi@smartlms.com", "Andi", "Pratama"),
            ("bella_mhs", "bella@smartlms.com", "Bella", "Putri"),
            ("charlie_mhs", "charlie@smartlms.com", "Charlie", "Wang"),
            ("dina_mhs", "dina@smartlms.com", "Dina", "Sari"),
            ("eko_mhs", "eko@smartlms.com", "Eko", "Prabowo"),
        ]
        for username, email, first, last in student_data:
            student = User.objects.create_user(
                username=username,
                email=email,
                password="student123",
                role=User.Role.STUDENT,
                first_name=first,
                last_name=last,
            )
            students.append(student)

        # Create Courses
        self.stdout.write("Creating courses...")
        courses = []
        course_titles = [
            ("Pemrograman Python Dasar", "Programming", 0),
            ("Web Development dengan Django", "Web Development", 150000),
            ("Basis Data PostgreSQL", "Database", 100000),
            ("Pemrograman Berorientasi Objek", "Programming", 120000),
            ("Desain UI/UX untuk Pemula", "Design", 80000),
            ("Machine Learning Dasar", "Data Science", 200000),
            ("Jaringan Komputer", "Networking", 90000),
            ("Sistem Operasi", "Operating System", 110000),
        ]

        for idx, (title, category, price) in enumerate(course_titles):
            course = Course.objects.create(
                title=title,
                slug=slugify(title),
                teacher=teachers[idx % 2],
                category=category,
                price=price,
                description=f"Kursus {title} yang komprehensif untuk pemula dan menengah.",
                status=Course.Status.PUBLISHED,
            )
            courses.append(course)

            # Add teacher as course member
            CourseMember.objects.get_or_create(
                course=course,
                user=course.teacher,
                defaults={"role": CourseMember.Role.TEACHER},
            )

        # Create Course Contents for each course
        self.stdout.write("Creating course contents...")
        content_titles = [
            "Pengenalan Konsep Dasar",
            "Praktikum Pertama",
            "Studi Kasus dan Tugas",
        ]
        for course in courses:
            for order, content_title in enumerate(content_titles, start=1):
                CourseContent.objects.create(
                    course=course,
                    title=f"{content_title} - {course.title}",
                    description=f"Materi untuk {content_title.lower()} pada kursus {course.title}.",
                    order=order,
                )

        # Create Enrollments: each student enrolls in 3-4 courses
        self.stdout.write("Creating enrollments and course members...")
        for student in students:
            selected_courses = random.sample(courses, k=random.randint(3, 4))
            for course in selected_courses:
                Enrollment.objects.get_or_create(
                    course=course,
                    student=student,
                    defaults={"is_active": True},
                )
                CourseMember.objects.get_or_create(
                    course=course,
                    user=student,
                    defaults={"role": CourseMember.Role.STUDENT},
                )

        # Create Comments: 3 comments per course
        self.stdout.write("Creating comments...")
        comment_texts = [
            "Materinya sangat jelas dan mudah dipahami!",
            "Kursus yang bermanfaat, saya sangat merekomendasikan.",
            "Pengajar menjelaskan dengan baik, terima kasih!",
            "Saya belajar banyak dari kursus ini.",
            "Kontennya terstruktur dengan rapi.",
        ]
        for course in courses:
            contents = list(course.contents.all())
            # Get only enrolled students for this course
            enrolled_students = [
                enrollment.student
                for enrollment in Enrollment.objects.filter(course=course, is_active=True)
            ]
            for _ in range(3):
                if enrolled_students and contents:
                    student = random.choice(enrolled_students)
                    content = random.choice(contents)
                    Comment.objects.create(
                        course=course,
                        content=content,
                        user=student,
                        text=random.choice(comment_texts),
                    )

        self.stdout.write(self.style.SUCCESS("Data seeding completed successfully!"))
        self.stdout.write(f"- {User.objects.count()} users created")
        self.stdout.write(f"- {Course.objects.count()} courses created")
        self.stdout.write(f"- {CourseContent.objects.count()} course contents created")
        self.stdout.write(f"- {Enrollment.objects.count()} enrollments created")
        self.stdout.write(f"- {Comment.objects.count()} comments created")
