# LAPORAN UJIAN AKHIR SEMESTER
## MATA KULIAH: PEMROGRAMAN SISI SERVER
### NAMA PROYEK: SMART LEARNING MANAGEMENT SYSTEM (SMART LMS)
### TEKNOLOGI: DJANGO 5, DJANGO NINJA, POSTGRESQL, BOOTSTRAP 5, JWT, DOCKER, RAILWAY

---

## KATA PENGANTAR

Puji syukur kehadirat Tuhan Yang Maha Esa, atas rahmat dan karunia-Nya, penulis dapat menyelesaikan proyek Ujian Akhir Semester mata kuliah Pemrograman Sisi Server dengan judul "Smart Learning Management System (Smart LMS)". Proyek ini bertujuan untuk membuat sistem manajemen pembelajaran berbasis web yang modern, scalable, dan mudah digunakan.

Proyek Smart LMS dirancang dengan arsitektur Model-View-Template (MVT) dari Django, dengan REST API menggunakan Django Ninja untuk menyediakan layanan backend yang robust. Sistem ini mendukung otentikasi JWT, role-based access control, filtering, sorting, pagination, dan fitur-fitur lainnya yang dibutuhkan untuk platform pembelajaran online.

---

## DAFTAR ISI

1. [LATAR BELAKANG](#1-latar-belakang)
2. [ANALISIS DAN RANCANGAN APLIKASI](#2-analisis-dan-rancangan-aplikasi)
3. [PEMODELAN UML](#3-pemodelan-uml)
4. [ANALISIS KEBUTUHAN](#4-analisis-kebutuhan)
5. [ANALISIS KEBUTUHAN HARDWARE DAN SOFTWARE](#5-analisis-kebutuhan-hardware-dan-software)
6. [SKEMA DIAGRAM RELASI TABEL](#6-skema-diagram-relasi-tabel)
7. [MODEL](#7-model)
8. [QUERY](#8-query)
9. [IMPORT CSV](#9-import-csv)
10. [API](#10-api)
11. [AUTH](#11-auth)
12. [THROTTLING, PAGINATION, FILTERING, SORTING](#12-throttling-pagination-filtering-sorting)
13. [DOCS](#13-docs)
14. [UNIT TESTING](#14-unit-testing)
15. [IMPLEMENTASI SISTEM](#15-implementasi-sistem)
16. [PENUTUP](#16-penutup)
17. [LAMPIRAN KODE PROGRAM](#17-lampiran-kode-program)

---

## 1. LATAR BELAKANG

Di era digital saat ini, pembelajaran online telah menjadi kebutuhan utama di dunia pendidikan. Sistem Manajemen Pembelajaran (Learning Management System/LMS) adalah platform yang memfasilitasi proses pembelajaran secara online dengan menyediakan fitur-fitur seperti manajemen kursus, konten pembelajaran, interaksi antar pengguna, dan monitoring pembelajaran.

Proyek Smart LMS dibuat untuk memenuhi kebutuhan tersebut dengan menggunakan teknologi modern seperti Django 5 sebagai web framework, Django Ninja sebagai REST API framework, PostgreSQL sebagai database, dan Bootstrap 5 untuk antarmuka pengguna. Sistem ini dirancang agar dapat diakses oleh berbagai peran pengguna seperti Admin, Guru (Teacher), dan Siswa (Student) dengan batasan akses yang sesuai.

Beberapa alasan utama pengembangan Smart LMS:
1. **Kebutuhan Platform Pembelajaran Modern**: Sistem pembelajaran yang mudah diakses dan user-friendly
2. **Role-Based Access Control**: Pengelolaan akses berdasarkan peran pengguna
3. **REST API untuk Integrasi**: Memungkinkan integrasi dengan frontend mobile atau pihak ketiga
4. **Scalability**: Arsitektur yang dapat dikembangkan sesuai kebutuhan
5. **Dokumentasi API Otomatis**: Memudahkan pengembang dalam penggunaan API

---

## 2. ANALISIS DAN RANCANGAN APLIKASI

### 2.1 Tujuan Proyek
- Membuat sistem manajemen pembelajaran berbasis web yang modern dan scalable
- Menyediakan REST API yang robust dan terdocumentasi dengan baik
- Mengimplementasikan otentikasi dan otorisasi berbasis JWT
- Menyediakan fitur filtering, sorting, dan pagination untuk manajemen data
- Membuat antarmuka pengguna yang responsif dengan Bootstrap 5

### 2.2 Arsitektur Sistem
Proyek Smart LMS menggunakan arsitektur **Model-View-Template (MVT)** dari Django dengan tambahan **REST API** menggunakan Django Ninja.

#### Arsitektur Umum:
```
┌─────────────────────────────────────────────────────────┐
│                      CLIENT SIDE                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Browser    │  │   Postman    │  │  Mobile App  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼──────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────┐
│                   SERVER SIDE (DJANGO)                    │
│  ┌─────────────────────────────────────────────────────┐ │
│  │                  URL ROUTER                         │ │
│  └──────────────────┬──────────────────────────────────┘ │
│  ┌──────────────────┼──────────────────────────────────┐ │
│  │     FRONTEND     │           REST API                │ │
│  │   (DJANGO VIEW)  │      (DJANGO NINJA)               │ │
│  └──────────────────┼──────────────────────────────────┘ │
│  ┌──────────────────┼──────────────────────────────────┐ │
│  │                  MODEL LAYER                        │ │
│  └──────────────────┼──────────────────────────────────┘ │
│  ┌──────────────────┼──────────────────────────────────┐ │
│  │              DATABASE (POSTGRESQL)                  │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

### 2.3 Struktur Direktori Proyek
```
smartlms_uas/
├── appmongo/                      # Konfigurasi project utama
│   ├── __init__.py
│   ├── api.py                     # API utama (Django Ninja)
│   ├── settings.py                # Pengaturan project
│   ├── urls.py                    # URL routing utama
│   ├── frontend_urls.py           # URL routing frontend
│   ├── views.py                   # Views untuk frontend
│   └── wsgi.py
├── apps/                          # Aplikasi Django
│   ├── accounts/                  # Manajemen User & Autentikasi
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── api/
│   │   ├── management/
│   │   ├── tests/
│   │   └── ...
│   ├── courses/                   # Manajemen Kursus
│   ├── contents/                  # Manajemen Konten Kursus
│   ├── comments/                  # Manajemen Komentar
│   ├── members/                   # Manajemen Anggota Kursus
│   ├── dashboard/                 # Dashboard
│   └── common/                    # Utility & Middleware
├── templates/                     # Template HTML
│   ├── layouts/
│   ├── courses/
│   ├── accounts/
│   └── ...
├── staticfiles/                   # File static
├── manage.py                      # Django manage script
├── requirements.txt               # Dependencies
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose
└── README.md
```

---

## 3. PEMODELAN UML

### 3.1 Use Case Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        SMART LMS                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐        ┌──────────┐        ┌──────────┐     │
│  │  ADMIN   │        │ TEACHER  │        │ STUDENT  │     │
│  └─────┬────┘        └─────┬────┘        └─────┬────┘     │
│        │                  │                  │            │
│        │ ◄─ Manage Users  │                  │            │
│        │ ◄─ Manage Courses│ ◄─ Create Course │            │
│        │                  │ ◄─ Edit Course   │            │
│        │                  │ ◄─ Add Content   │            │
│        │                  │                  │ ◄─ View    │
│        │                  │                  │    Courses │
│        │                  │                  │ ◄─ Join    │
│        │                  │                  │    Course  │
│        │                  │                  │ ◄─ View    │
│        │                  │                  │    Content │
│        │                  │                  │ ◄─ Comment │
│        │                  │                  │            │
└────────┼──────────────────┼──────────────────┼────────────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                     ┌──────▼──────┐
                     │   GUEST     │
                     │ (Not Login) │
                     └─────────────┘
                        ◄─ View Courses
```

### 3.2 Class Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                              User                                   │
├─────────────────────────────────────────────────────────────────────┤
│ - id: BigAutoField (PK)                                             │
│ - username: CharField (unique)                                      │
│ - email: EmailField (unique)                                        │
│ - password: CharField                                               │
│ - role: CharField (ADMIN/TEACHER/STUDENT)                           │
│ - avatar: ImageField (optional)                                     │
│ - bio: TextField (optional)                                         │
│ - first_name: CharField                                             │
│ - last_name: CharField                                              │
│ - is_staff: BooleanField                                            │
│ - is_superuser: BooleanField                                        │
│ - is_active: BooleanField                                           │
│ - date_joined: DateTimeField                                        │
├─────────────────────────────────────────────────────────────────────┤
│ + __str__(): str                                                    │
└─────────────────────────────────────────────────────────────────────┘
                              ▲
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         │                    │                    │
┌────────┴────────┐  ┌────────┴────────┐  ┌──────┴───────┐
│    Course       │  │  CourseContent  │  │ CourseMember │
├─────────────────┤  ├─────────────────┤  ├──────────────┤
│ - id (PK)       │  │ - id (PK)       │  │ - id (PK)    │
│ - title         │  │ - course (FK)   │  │ - course (FK)│
│ - slug (unique) │  │ - title         │  │ - user (FK)  │
│ - teacher (FK)  │  │ - description   │  │ - role       │
│ - category      │  │ - video_url     │  │ - joined_at  │
│ - price         │  │ - attachment    │  └──────────────┘
│ - description   │  │ - order         │         ▲
│ - status        │  │ - created_at    │         │
│ - created_at    │  │ - updated_at    │         │
│ - updated_at    │  └─────────────────┘  ┌──────┴───────┐
├─────────────────┤                       │   Enrollment  │
│ + __str__()     │                       ├──────────────┤
│ + name (property)│                      │ - id (PK)    │
└─────────────────┘                       │ - course (FK)│
         ▲                                │ - student (FK)│
         │                                │ - enrolled_at│
         │                                │ - is_active  │
┌────────┴────────┐                       └──────────────┘
│    Comment      │                              ▲
├─────────────────┤                              │
│ - id (PK)       │                              │
│ - course (FK)   │                              │
│ - content (FK)  │                              │
│ - user (FK)     │                              │
│ - parent (FK)   │                              │
│ - text          │                              │
│ - created_at    │                              │
│ - updated_at    │                              │
├─────────────────┤                              │
│ + __str__()     │                              │
└─────────────────┘                              │
                                                 │
```

---

## 4. ANALISIS KEBUTUHAN

### 4.1 Kebutuhan Fungsional

#### 4.1.1 Untuk Semua Pengguna (Guest)
- Melihat daftar kursus yang dipublikasikan
- Melihat detail kursus
- Mencari kursus berdasarkan judul, deskripsi, atau pengajar
- Memfilter kursus berdasarkan kategori dan harga
- Mengurutkan kursus berdasarkan tanggal dibuat, harga, atau judul

#### 4.1.2 Untuk Siswa (Student)
- Semua fitur Guest
- Login ke sistem
- Mendaftar (enroll) ke kursus
- Melihat daftar kursus yang diikuti
- Melihat konten kursus yang diikuti
- Memberikan komentar pada konten kursus
- Melihat dashboard siswa

#### 4.1.3 Untuk Guru (Teacher)
- Semua fitur Siswa
- Membuat kursus baru
- Mengedit dan menghapus kursus sendiri
- Menambahkan konten ke kursus
- Mengedit dan menghapus konten kursus
- Melihat anggota kursus
- Melihat dashboard guru

#### 4.1.4 Untuk Admin
- Semua fitur Guru
- Mengelola semua pengguna (CRUD)
- Mengelola semua kursus (CRUD)
- Melihat statistik sistem
- Mengakses Django Admin Panel

### 4.2 Kebutuhan Non-Fungsional
1. **Performa**: API harus merespon dalam waktu kurang dari 2 detik
2. **Keamanan**: Menggunakan JWT untuk otentikasi, CSRF protection, dan password hashing
3. **Scalability**: Dapat menangani peningkatan jumlah pengguna dan data
4. **Ketersediaan**: Sistem harus tersedia 99% waktu
5. **Dokumentasi**: API harus terdocumentasi dengan baik menggunakan Swagger/OpenAPI
6. **Responsif**: Antarmuka pengguna harus responsif di berbagai perangkat

---

## 5. ANALISIS KEBUTUHAN HARDWARE DAN SOFTWARE

### 5.1 Kebutuhan Hardware

#### Untuk Pengembangan (Development)
- **Processor**: Minimal Intel Core i3 atau AMD equivalent
- **RAM**: Minimal 4 GB (Rekomendasi 8 GB)
- **Storage**: Minimal 10 GB ruang kosong
- **Jaringan**: Koneksi internet untuk mengunduh dependencies

#### Untuk Production (Railway)
- **Processor**: 1-2 vCPU
- **RAM**: 512 MB - 2 GB
- **Storage**: 1-10 GB
- **Database**: PostgreSQL dengan minimal 1 GB storage

### 5.2 Kebutuhan Software

#### Untuk Pengembangan
| Software | Versi | Keterangan |
|----------|-------|------------|
| Python | 3.8+ | Bahasa pemrograman |
| Django | 5.0+ | Web framework |
| Django Ninja | 1.1+ | REST API framework |
| PostgreSQL | 13+ | Database (opsional SQLite untuk dev) |
| Git | Terbaru | Version control |
| Browser | Chrome/Firefox | Testing frontend |
| Code Editor | VS Code/PyCharm | Penulisan kode |

#### Untuk Production
| Software | Versi | Keterangan |
|----------|-------|------------|
| Python | 3.8+ | Runtime |
| Gunicorn | 22.0+ | WSGI Server |
| PostgreSQL | 13+ | Database |
| Nginx (opsional) | Terbaru | Reverse proxy |
| Docker | Terbaru | Containerization |
| Whitenoise | Terbaru | Static file serving |

---

## 6. SKEMA DIAGRAM RELASI TABEL

### 6.1 Entity Relationship Diagram (ERD)

```
┌─────────────────┐         ┌─────────────────┐
│      User       │         │     Course      │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │◄────────│ teacher_id (FK) │
│ username        │         │ id (PK)         │
│ email           │         │ title           │
│ password        │         │ slug            │
│ role            │         │ category        │
│ avatar          │         │ price           │
│ bio             │         │ description     │
│ first_name      │         │ status          │
│ last_name       │         │ created_at      │
│ is_staff        │         │ updated_at      │
│ is_superuser    │         └────────┬────────┘
│ is_active       │                  │
│ date_joined     │                  │
└─────────────────┘                  │
         ▲                           │
         │                           │
         │                           │
┌────────┴────────┐         ┌────────┴────────┐
│  CourseMember   │         │  CourseContent  │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │◄────────│ course_id (FK)  │
│ course_id (FK)  │         │ id (PK)         │
│ user_id (FK)    │         │ title           │
│ role            │         │ description     │
│ joined_at       │         │ video_url       │
└─────────────────┘         │ attachment      │
         ▲                   │ order           │
         │                   │ created_at      │
         │                   │ updated_at      │
┌────────┴────────┐         └────────┬────────┘
│   Enrollment    │                  │
├─────────────────┤                  │
│ id (PK)         │◄─────────────────┘
│ course_id (FK)  │
│ student_id (FK) │
│ enrolled_at     │
│ is_active       │
└─────────────────┘         ┌─────────────────┐
         ▲                  │     Comment     │
         │                  ├─────────────────┤
         └─────────────────►│ course_id (FK)  │
                            │ content_id (FK) │
                            │ user_id (FK)    │
                            │ parent_id (FK)  │
                            │ text            │
                            │ created_at      │
                            │ updated_at      │
                            └─────────────────┘
```

### 6.2 Penjelasan Relasi

1. **User ↔ Course**: One-to-Many (Satu user dapat memiliki banyak course sebagai teacher)
2. **Course ↔ CourseContent**: One-to-Many (Satu course dapat memiliki banyak content)
3. **Course ↔ CourseMember**: One-to-Many (Satu course dapat memiliki banyak member)
4. **User ↔ CourseMember**: One-to-Many (Satu user dapat menjadi member di banyak course)
5. **Course ↔ Enrollment**: One-to-Many (Satu course dapat memiliki banyak enrollment)
6. **User ↔ Enrollment**: One-to-Many (Satu user dapat enroll di banyak course)
7. **Course ↔ Comment**: One-to-Many (Satu course dapat memiliki banyak comment)
8. **CourseContent ↔ Comment**: One-to-Many (Satu content dapat memiliki banyak comment)
9. **User ↔ Comment**: One-to-Many (Satu user dapat membuat banyak comment)
10. **Comment ↔ Comment**: Self-Referential (Satu comment dapat memiliki banyak balasan)

---

## 7. MODEL

### 7.1 Model User (apps/accounts/models.py)

Model kustom User yang mewarisi `AbstractUser` dengan penambahan field `role`, `avatar`, dan `bio`.

```python
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        TEACHER = "teacher", "Teacher"
        STUDENT = "student", "Student"

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[MinLengthValidator(5)],
        verbose_name="Username",
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        db_index=True,
        verbose_name="Role",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Avatar",
    )
    bio = models.TextField(blank=True, verbose_name="Bio")

    class Meta:
        ordering = ["username"]
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["username"], name="user_username_idx"),
            models.Index(fields=["email"], name="user_email_idx"),
            models.Index(fields=["role"], name="user_role_idx"),
        ]

    def __str__(self):
        return f"{self.username} ({self.role})"
```

### 7.2 Model Course (apps/courses/models.py)

Model untuk menyimpan data kursus dengan field `title`, `slug`, `teacher`, `category`, `price`, `description`, dan `status`.

```python
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
```

### 7.3 Model CourseContent (apps/contents/models.py)

Model untuk menyimpan konten kursus seperti materi, video, dan file attachment.

```python
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
```

### 7.4 Model CourseMember dan Enrollment (apps/members/models.py)

Model untuk mengelola anggota kursus dan pendaftaran kursus.

```python
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
```

### 7.5 Model Comment (apps/comments/models.py)

Model untuk menyimpan komentar pengguna pada konten kursus.

```python
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
```

---

## 8. QUERY

### 8.1 Query Optimisasi dengan select_related dan prefetch_related

Proyek Smart LMS menggunakan `select_related` untuk foreign key dan `prefetch_related` untuk many-to-many dan reverse foreign key untuk mengoptimasi query dan menghindari N+1 query problem.

#### Contoh Query Course dengan Relasi:

```python
# apps/courses/api/router.py
def course_queryset():
    return Course.objects.select_related("teacher").annotate(
        content_count=Count("contents", distinct=True),
        member_count=Count("members", distinct=True),
        comment_count=Count("comments", distinct=True),
    )
```

### 8.2 Query Filtering dengan Q Objects

Untuk pencarian multi-field, menggunakan `Q` objects dari Django:

```python
# apps/courses/api/schemas.py (FilterSchema)
class CourseFilterSchema(FilterSchema):
    search: Optional[str] = None
    price_gte: Optional[Decimal] = None
    price_lte: Optional[Decimal] = None
    category: Optional[str] = None
    status: Optional[str] = None

    def filter_search(self, search: Optional[str]) -> Q:
        if not search:
            return Q()
        return Q(title__icontains=search) | Q(description__icontains=search) | Q(teacher__username__icontains=search)

    def filter_price_gte(self, price_gte: Optional[Decimal]) -> Q:
        if price_gte is None:
            return Q()
        return Q(price__gte=price_gte)

    def filter_price_lte(self, price_lte: Optional[Decimal]) -> Q:
        if price_lte is None:
            return Q()
        return Q(price__lte=price_lte)
```

### 8.3 Query Aggregation dan Annotation

Menggunakan `annotate` untuk menghitung jumlah konten, member, dan komentar pada setiap course:

```python
from django.db.models import Count

course_queryset = Course.objects.select_related("teacher").annotate(
    content_count=Count("contents", distinct=True),
    member_count=Count("members", distinct=True),
    comment_count=Count("comments", distinct=True),
)
```

### 8.4 Query untuk Cek Enrollment

```python
from apps.members.models import Enrollment

is_enrolled = Enrollment.objects.filter(
    course_id=course_id,
    student_id=user_id,
    is_active=True,
).exists()
```

---

## 9. IMPORT CSV

Meskipun proyek Smart LMS tidak memiliki fitur import CSV secara eksplisit, berikut adalah contoh implementasi management command untuk import data dari CSV:

### Contoh Management Command Import CSV:

```python
# apps/accounts/management/commands/import_users.py
import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Import users from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to CSV file")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                User.objects.get_or_create(
                    username=row["username"],
                    defaults={
                        "email": row["email"],
                        "first_name": row.get("first_name", ""),
                        "last_name": row.get("last_name", ""),
                        "role": row.get("role", User.Role.STUDENT),
                    }
                )
                if "password" in row:
                    user = User.objects.get(username=row["username"])
                    user.set_password(row["password"])
                    user.save()
        
        self.stdout.write(self.style.SUCCESS("Users imported successfully!"))
```

Namun, proyek Smart LMS sudah memiliki management command `seed_data` untuk mengisi data dummy secara otomatis (lihat [Lampiran](#17-lampiran-kode-program)).

---

## 10. API

### 10.1 Struktur API

Proyek Smart LMS menggunakan **Django Ninja** sebagai REST API framework dengan base URL `/api/v1/`.

#### Struktur Router API:

```python
# appmongo/api.py
from ninja import NinjaAPI
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth

from apps.accounts.api.router import router as accounts_router
from apps.accounts.api.users_router import router as users_router
from apps.comments.api.router import router as comments_router
from apps.contents.api.router import router as contents_router
from apps.courses.api.router import router as courses_router
from apps.dashboard.api.router import router as dashboard_router
from apps.dashboard.api.statistics_router import router as statistics_router
from apps.members.api.router import router as members_router

apiAuth = HttpJwtAuth()

api = NinjaAPI(
    title="Smart LMS",
    version="1.0.0",
    description="Smart Learning Management System API untuk UAS Pemrograman Sisi Server",
    urls_namespace="smart_lms_api",
    auth=apiAuth,
)

api.add_router("/auth/", accounts_router)
api.add_router("/users/", users_router)
api.add_router("/courses/", courses_router)
api.add_router("/course-members/", members_router)
api.add_router("/course-contents/", contents_router)
api.add_router("/comments/", comments_router)
api.add_router("/dashboard/", dashboard_router)
api.add_router("/statistics/", statistics_router)
```

### 10.2 Daftar Endpoint API

#### 10.2.1 Autentikasi (`/api/v1/auth/`)

| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| POST | `/login` | Login dan mendapatkan access & refresh token | No |
| POST | `/refresh` | Refresh access token | No |
| POST | `/logout` | Logout (blacklist token) | Yes |

#### 10.2.2 Courses (`/api/v1/courses/`)

| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| GET | `/` | List semua course dengan filter, sort, pagination | No |
| GET | `/{course_id}` | Detail course beserta konten dan member | No |
| POST | `/` | Buat course baru | Teacher/Admin |
| PATCH | `/{course_id}` | Update course | Teacher/Admin |
| DELETE | `/{course_id}` | Hapus course | Teacher/Admin |

#### 10.2.3 Course Contents (`/api/v1/course-contents/`)

| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| GET | `/` | List semua content | Yes |
| GET | `/{content_id}` | Detail content | Yes |
| POST | `/` | Buat content baru | Teacher/Admin |
| PATCH | `/{content_id}` | Update content | Teacher/Admin |
| DELETE | `/{content_id}` | Hapus content | Teacher/Admin |

#### 10.2.4 Course Members (`/api/v1/course-members/`)

| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| GET | `/` | List member course | Yes |
| POST | `/` | Tambah member ke course | Teacher/Admin |
| DELETE | `/{member_id}` | Hapus member dari course | Teacher/Admin |

#### 10.2.5 Comments (`/api/v1/comments/`)

| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| GET | `/` | List comment | Yes |
| POST | `/` | Buat comment baru | Yes |
| PATCH | `/{comment_id}` | Update comment | Yes (owner) |
| DELETE | `/{comment_id}` | Hapus comment | Yes (owner) |

#### 10.2.6 Statistics (`/api/v1/statistics/`)

| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| GET | `/` | Get statistik sistem | Admin |

### 10.3 Contoh Request dan Response API

#### Contoh 1: Login
**Request:**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Contoh 2: Get List Courses dengan Filter dan Sort
**Request:**
```http
GET /api/v1/courses/?search=django&price_gte=0&price_lte=200000&sort_by=price_asc&page=1&page_size=5
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "count": 8,
  "page": 1,
  "page_size": 5,
  "results": [
    {
      "id": 1,
      "title": "Pemrograman Python Dasar",
      "slug": "pemrograman-python-dasar",
      "teacher_username": "budi_guru",
      "category": "Programming",
      "price": "0.00",
      "status": "published",
      "content_count": 3,
      "member_count": 4,
      "comment_count": 3
    }
  ]
}
```

#### Contoh 3: Buat Course Baru
**Request:**
```http
POST /api/v1/courses/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Kursus Baru",
  "category": "Programming",
  "price": 100000,
  "description": "Deskripsi kursus baru",
  "status": "draft"
}
```

**Response (201 Created):**
```json
{
  "id": 9,
  "title": "Kursus Baru",
  "slug": "kursus-baru",
  "teacher_username": "budi_guru",
  "category": "Programming",
  "price": "100000.00",
  "status": "draft",
  "content_count": 0,
  "member_count": 1,
  "comment_count": 0
}
```

---

## 11. AUTH

### 11.1 JWT Authentication

Proyek Smart LMS menggunakan **django-ninja-simple-jwt** untuk otentikasi berbasis JSON Web Token (JWT).

#### Konfigurasi JWT di settings.py:

```python
# appmongo/settings.py
from datetime import timedelta

NINJA_SIMPLE_JWT = {
    "JWT_PRIVATE_KEY": SECRET_KEY,
    "JWT_PUBLIC_KEY": SECRET_KEY,
    "JWT_ALGORITHM": "HS256",
    "JWT_ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "JWT_REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "USE_STATELESS_AUTH": False,
    "TOKEN_CLAIM_USER_ATTRIBUTE_MAP": {
        "user_id": "id",
        "username": "username",
        "email": "email",
        "first_name": "first_name",
        "last_name": "last_name",
        "role": "role",
        "is_staff": "is_staff",
        "is_superuser": "is_superuser",
        "is_active": "is_active",
    },
}
```

### 11.2 Alur Otentikasi

1. **Login**: User mengirim username dan password ke `/api/v1/auth/login`
2. **Response**: Server mengembalikan `access_token` (valid 15 menit) dan `refresh_token` (valid 7 hari)
3. **Authenticated Request**: Client mengirim `access_token` di header `Authorization: Bearer <access_token>`
4. **Refresh Token**: Ketika `access_token` kedaluwarsa, client gunakan `refresh_token` untuk mendapatkan `access_token` baru
5. **Logout**: Client mengirim `refresh_token` ke `/api/v1/auth/logout` untuk blacklist token

### 11.3 Role-Based Authorization

Proyek Smart LMS menerapkan otorisasi berbasis peran (role):

#### Decorator untuk Memeriksa Role:

```python
# apps/common/api/utils.py
from ninja.errors import HttpError


def require_teacher(request):
    user = request.auth
    if user.role not in [User.Role.TEACHER, User.Role.ADMIN]:
        raise HttpError(403, "Teacher or Admin role required.")
    return user
```

#### Contoh Penggunaan di Endpoint:

```python
# apps/courses/api/router.py
@router.post("/", response={201: CourseOutSchema})
@transaction.atomic
def create_course(request, payload: CourseCreateSchema):
    teacher = require_teacher(request)  # Hanya teacher/admin yang bisa akses
    # ... logic create course
```

### 11.4 Pengaturan User Model Kustom

```python
# appmongo/settings.py
AUTH_USER_MODEL = "accounts.User"
```

---

## 12. THROTTLING, PAGINATION, FILTERING, SORTING

### 12.1 Throttling (Rate Limiting)

Proyek Smart LMS memiliki custom middleware untuk rate limiting guna mencegah abuse API.

#### Implementasi Middleware:

```python
# apps/common/middleware.py
import time
from django.core.cache import cache
from django.http import JsonResponse


class ApiRateLimitMiddleware:
    window_seconds = 60
    anonymous_limit = 10
    authenticated_limit = 100
    login_limit = 5

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/v1/"):
            response = self.rate_limit(request)
            if response:
                return response
        return self.get_response(request)

    def rate_limit(self, request):
        now = int(time.time())
        window = now // self.window_seconds
        identity = self.identity(request)
        limit = self.login_limit if request.path == "/api/v1/auth/login" else self.request_limit(request)
        cache_key = f"throttle:{request.path}:{identity}:{window}"
        count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, count, timeout=self.window_seconds)
        if count > limit:
            return JsonResponse(
                {"detail": "Request was throttled. Please try again later."},
                status=429,
                headers={"Retry-After": str(self.window_seconds)},
            )
        return None

    def request_limit(self, request):
        return self.authenticated_limit if request.headers.get("Authorization") else self.anonymous_limit

    def identity(self, request):
        auth = request.headers.get("Authorization")
        if auth:
            return f"auth:{auth[-24:]}"
        return f"anon:{request.META.get('REMOTE_ADDR', 'unknown')}"
```

#### Batas Rate Limiting:
- **Anonymous User**: 10 request per menit
- **Authenticated User**: 100 request per menit
- **Login Endpoint**: 5 request per menit (untuk mencegah brute force)

### 12.2 Pagination

Pagination diterapkan pada endpoint list untuk memecah data menjadi halaman-halaman.

#### Implementasi Pagination:

```python
# apps/common/api/utils.py
from django.core.paginator import Paginator


def paginate_queryset(queryset, page: int, page_size: int):
    page_size = min(page_size, 50)  # Max 50 items per page
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    return {
        "count": paginator.count,
        "page": page_obj.number,
        "page_size": page_size,
        "results": list(page_obj),
    }
```

#### Parameter Pagination:
- `page`: Nomor halaman (default: 1)
- `page_size`: Jumlah item per halaman (default: 5, max: 50)

### 12.3 Filtering

Filtering menggunakan `FilterSchema` dari Django Ninja.

#### Implementasi Filter Schema:

```python
# apps/courses/api/schemas.py
from ninja import FilterSchema
from django.db.models import Q
from typing import Optional
from decimal import Decimal


class CourseFilterSchema(FilterSchema):
    search: Optional[str] = None
    price_gte: Optional[Decimal] = None
    price_lte: Optional[Decimal] = None
    category: Optional[str] = None
    status: Optional[str] = None

    def filter_search(self, search: Optional[str]) -> Q:
        if not search:
            return Q()
        return Q(title__icontains=search) | Q(description__icontains=search) | Q(teacher__username__icontains=search)

    def filter_price_gte(self, price_gte: Optional[Decimal]) -> Q:
        if price_gte is None:
            return Q()
        return Q(price__gte=price_gte)

    def filter_price_lte(self, price_lte: Optional[Decimal]) -> Q:
        if price_lte is None:
            return Q()
        return Q(price__lte=price_lte)

    def filter_category(self, category: Optional[str]) -> Q:
        if not category:
            return Q()
        return Q(category__iexact=category)

    def filter_status(self, status: Optional[str]) -> Q:
        if not status:
            return Q()
        return Q(status__iexact=status)
```

#### Parameter Filter:
- `search`: Pencarian berdasarkan title, description, atau teacher username
- `price_gte`: Harga minimum
- `price_lte`: Harga maksimum
- `category`: Kategori kursus
- `status`: Status kursus (draft/published/archived)

### 12.4 Sorting

Sorting dapat dilakukan dengan parameter `sort_by`.

#### Implementasi Sorting:

```python
# apps/courses/api/router.py
@router.get("/", response=CourseListSchema, auth=None)
def list_courses(
    request,
    filters: CourseFilterSchema = Query(...),
    sort_by: str = Query("created_at", alias="sort_by"),
    page: int = 1,
    page_size: int = Query(5, alias="page_size"),
):
    queryset = course_queryset()
    queryset = filters.filter(queryset)
    
    # Apply sorting
    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort_by == 'title_asc' or sort_by == 'name_asc':
        queryset = queryset.order_by('title')
    elif sort_by == 'title_desc' or sort_by == 'name_desc':
        queryset = queryset.order_by('-title')
    else:  # Default: created_at
        queryset = queryset.order_by('-created_at')
    
    return paginate_queryset(queryset, page, page_size)
```

#### Parameter Sort:
- `created_at`: Urutkan berdasarkan tanggal dibuat (default, descending)
- `price_asc`: Urutkan berdasarkan harga (ascending)
- `price_desc`: Urutkan berdasarkan harga (descending)
- `title_asc` / `name_asc`: Urutkan berdasarkan judul (ascending)
- `title_desc` / `name_desc`: Urutkan berdasarkan judul (descending)

---

## 13. DOCS

### 13.1 Dokumentasi API dengan Swagger/OpenAPI

Django Ninja secara otomatis menghasilkan dokumentasi API menggunakan **Swagger UI** dan **OpenAPI Schema**.

#### Akses Dokumentasi:
- **Swagger UI**: `/api/v1/docs`
- **OpenAPI JSON**: `/api/v1/openapi.json`

#### Fitur Swagger UI:
1. **List Semua Endpoint**: Melihat semua endpoint yang tersedia
2. **Try it Out**: Mengeksekusi endpoint langsung dari browser
3. **Schema Request/Response**: Melihat struktur data request dan response
4. **Contoh Request/Response**: Melihat contoh penggunaan endpoint
5. **Autentikasi**: Memasukkan JWT token untuk menguji endpoint yang memerlukan otentikasi

#### Cara Menggunakan Swagger UI:
1. Buka `/api/v1/docs` di browser
2. Klik tombol **Authorize** di kanan atas
3. Masukkan `Bearer <access_token>` (dapatkan dari endpoint login)
4. Klik **Authorize** lalu **Close**
5. Pilih endpoint yang ingin diuji, klik **Try it out**
6. Isi parameter atau request body jika diperlukan
7. Klik **Execute** untuk melihat response

---

## 14. UNIT TESTING

### 14.1 Struktur Testing

Proyek Smart LMS memiliki unit test untuk masing-masing aplikasi:

```
apps/
├── accounts/tests/
│   └── test_auth.py
├── courses/tests/
│   └── test_courses.py
├── contents/tests/
│   └── test_contents.py
├── members/tests/
│   └── test_members.py
└── comments/tests/
    └── test_comments.py
```

### 14.2 Menjalankan Test

```bash
python manage.py test
```

### 14.3 Contoh Test Case

#### Contoh Test Autentikasi:

```python
# apps/accounts/tests/test_auth.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Role.STUDENT,
        )

    def test_login_success(self):
        url = reverse("api-1.0.0:accounts_login")
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        url = reverse("api-1.0.0:accounts_login")
        data = {
            "username": "testuser",
            "password": "wrongpass"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

#### Contoh Test Course API:

```python
# apps/courses/tests/test_courses.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from apps.courses.models import Course

User = get_user_model()


class CourseAPITests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
            role=User.Role.ADMIN,
        )
        self.teacher = User.objects.create_user(
            username="teacher1",
            email="teacher1@example.com",
            password="teacher123",
            role=User.Role.TEACHER,
        )
        self.student = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="student123",
            role=User.Role.STUDENT,
        )
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            teacher=self.teacher,
            category="Programming",
            price=100000,
            description="Test course description",
            status=Course.Status.PUBLISHED,
        )

    def test_list_courses_unauthenticated(self):
        url = reverse("api-1.0.0:courses_list_courses")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_teacher(self):
        url = reverse("api-1.0.0:courses_create_course")
        self.client.login(username="teacher1", password="teacher123")
        
        # Get token
        login_url = reverse("api-1.0.0:accounts_login")
        login_data = {"username": "teacher1", "password": "teacher123"}
        login_response = self.client.post(login_url, login_data, format="json")
        token = login_response.data["access"]
        
        # Create course
        data = {
            "title": "New Course",
            "category": "Programming",
            "price": 150000,
            "description": "New course description",
            "status": "draft"
        }
        response = self.client.post(
            url, 
            data, 
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_student_forbidden(self):
        url = reverse("api-1.0.0:courses_create_course")
        self.client.login(username="student1", password="student123")
        
        login_url = reverse("api-1.0.0:accounts_login")
        login_data = {"username": "student1", "password": "student123"}
        login_response = self.client.post(login_url, login_data, format="json")
        token = login_response.data["access"]
        
        data = {
            "title": "New Course",
            "category": "Programming",
            "price": 150000,
            "description": "New course description",
            "status": "draft"
        }
        response = self.client.post(
            url, 
            data, 
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

### 14.4 Cakupan Testing

Proyek Smart LMS memiliki total **41 test cases** yang mencakup:
1. **Model**: Testing validasi model dan method
2. **View**: Testing view frontend
3. **API**: Testing endpoint API (success dan error case)
4. **Autentikasi**: Testing login, logout, dan refresh token
5. **Otorisasi**: Testing role-based access control
6. **Throttling**: Testing rate limiting
7. **Filtering, Sorting, Pagination**: Testing fitur filtering, sorting, dan pagination

---

## 15. IMPLEMENTASI SISTEM

### 15.1 Instalasi dan Setup

#### Langkah 1: Clone Repository
```bash
git clone <repository-url>
cd smartlms_uas
```

#### Langkah 2: Buat Virtual Environment
```bash
python -m venv venv
```

#### Langkah 3: Aktifkan Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### Langkah 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Langkah 5: Konfigurasi Environment
Salin `.env.example` menjadi `.env` dan sesuaikan konfigurasi:
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=smart_lms
POSTGRES_USER=smart_lms_user
POSTGRES_PASSWORD=smart_lms_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

#### Langkah 6: Jalankan Migrasi Database
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Langkah 7: Seed Data Dummy
```bash
python manage.py seed_data
```

#### Langkah 8: Jalankan Server
```bash
python manage.py runserver
```

#### Langkah 9: Akses Aplikasi
- **Frontend**: `http://localhost:8000/`
- **Admin Panel**: `http://localhost:8000/admin/`
- **API Docs**: `http://localhost:8000/api/v1/docs`

### 15.2 Credential Awal (Setelah Seeding)

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Teacher | budi_guru | teacher123 |
| Teacher | siti_guru | teacher123 |
| Student | andi_mhs | student123 |
| Student | bella_mhs | student123 |
| Student | charlie_mhs | student123 |
| Student | dina_mhs | student123 |
| Student | eko_mhs | student123 |

### 15.3 Deployment ke Railway

Proyek Smart LMS dapat di-deploy ke Railway dengan mudah.

#### Langkah Deployment:
1. **Push kode ke GitHub/GitLab**
2. **Login ke Railway**: `railway.app`
3. **Buat Project Baru**
4. **Tambahkan Service PostgreSQL**
5. **Tambahkan Service GitHub Repository**
6. **Konfigurasi Environment Variables**:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS`
   - `DATABASE_URL` (otomatis dari Railway PostgreSQL)
7. **Deploy**
8. **Jalankan Migrasi**:
   ```bash
   railway run python manage.py migrate
   railway run python manage.py seed_data
   ```

### 15.4 Halaman Frontend

Proyek Smart LMS memiliki antarmuka frontend dengan Bootstrap 5 dan tema baby blue putih.

#### Daftar Halaman:
1. **Home (`/`)**: Halaman utama, daftar kursus populer
2. **Courses (`/courses/`)**: Daftar semua kursus dengan filter, search, sort, pagination
3. **Course Detail (`/courses/<id>/`)**: Detail kursus, tombol join, daftar konten
4. **Course Content List (`/courses/<id>/contents/`)**: Daftar konten kursus
5. **Content Detail (`/contents/<id>/`)**: Detail konten, komentar
6. **My Courses (`/my-courses/`)**: Daftar kursus yang diikuti user
7. **Dashboard (`/dashboard/`)**: Dashboard sesuai role
8. **Login (`/accounts/login/`)**: Halaman login
9. **Logout (`/accounts/logout/`)**: Logout

---

## 16. PENUTUP

### 16.1 Kesimpulan

Proyek Smart Learning Management System (Smart LMS) telah berhasil dikembangkan dengan menggunakan teknologi modern seperti Django 5, Django Ninja, PostgreSQL, Bootstrap 5, dan JWT Authentication. Sistem ini menyediakan fitur-fitur yang dibutuhkan untuk platform pembelajaran online seperti:

1. **Manajemen User dengan Role-Based Access Control**: Admin, Teacher, dan Student
2. **REST API yang Robust**: Menggunakan Django Ninja dengan dokumentasi otomatis Swagger
3. **Otentikasi JWT**: Aman dan scalable
4. **Filtering, Sorting, Pagination**: Untuk manajemen data yang efisien
5. **Throttling**: Mencegah abuse API
6. **Unit Testing**: 41 test cases untuk memastikan kualitas kode
7. **Antarmuka Pengguna Responsif**: Menggunakan Bootstrap 5
8. **Deployment Ready**: Dapat di-deploy ke Railway dengan Docker

### 16.2 Saran Pengembangan

Untuk pengembangan selanjutnya, beberapa fitur yang dapat ditambahkan:

1. **Notification System**: Notifikasi untuk pengguna ketika ada update kursus
2. **Quiz dan Assignment**: Fitur kuis dan tugas untuk evaluasi pembelajaran
3. **Certificate Generation**: Generate sertifikat setelah menyelesaikan kursus
4. **Payment Gateway**: Integrasi dengan payment gateway untuk kursus berbayar
5. **Video Streaming**: Streaming video untuk materi pembelajaran
6. **Real-time Chat**: Fitur chat antara guru dan siswa
7. **Analytics**: Dashboard analytics untuk melihat perkembangan pembelajaran
8. **Mobile App**: Aplikasi mobile untuk iOS dan Android

### 16.3 Ucapan Terima Kasih

Penulis mengucapkan terima kasih kepada:
- Dosen pengampu mata kuliah Pemrograman Sisi Server yang telah memberikan bimbingan dan ilmu
- Teman-teman yang telah membantu dalam pengembangan proyek ini
- Keluarga yang selalu memberikan dukungan dan doa

---

## 17. LAMPIRAN KODE PROGRAM

### Lampiran 1: File settings.py (appmongo/settings.py)

```python
import os
from pathlib import Path
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def env_list(name, default=None):
    value = os.getenv(name)
    if not value:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-smart-lms-development-secret-key-please-change",
)
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", ["localhost", "127.0.0.1", "testserver"])
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "ninja_simple_jwt",
    "apps.accounts",
    "apps.common",
    "apps.courses",
    "apps.contents",
    "apps.comments",
    "apps.members",
    "apps.dashboard",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "apps.common.middleware.ApiRateLimitMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "appmongo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "appmongo.wsgi.application"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "smart-lms-throttle",
    }
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "smart_lms"),
        "USER": os.getenv("POSTGRES_USER", "smart_lms_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "smart_lms_password"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

NINJA_SIMPLE_JWT = {
    "JWT_PRIVATE_KEY": SECRET_KEY,
    "JWT_PUBLIC_KEY": SECRET_KEY,
    "JWT_ALGORITHM": "HS256",
    "JWT_ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "JWT_REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "USE_STATELESS_AUTH": False,
    "TOKEN_CLAIM_USER_ATTRIBUTE_MAP": {
        "user_id": "id",
        "username": "username",
        "email": "email",
        "first_name": "first_name",
        "last_name": "last_name",
        "role": "role",
        "is_staff": "is_staff",
        "is_superuser": "is_superuser",
        "is_active": "is_active",
    },
}


LANGUAGE_CODE = "id-id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_DIR = BASE_DIR / "static"
if STATIC_DIR.exists():
    STATICFILES_DIRS = [STATIC_DIR]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### Lampiran 2: File api.py (appmongo/api.py)

```python
from ninja import NinjaAPI
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth

from apps.accounts.api.router import router as accounts_router
from apps.accounts.api.users_router import router as users_router
from apps.comments.api.router import router as comments_router
from apps.contents.api.router import router as contents_router
from apps.courses.api.router import router as courses_router
from apps.dashboard.api.router import router as dashboard_router
from apps.dashboard.api.statistics_router import router as statistics_router
from apps.members.api.router import router as members_router


apiAuth = HttpJwtAuth()

api = NinjaAPI(
    title="Smart LMS",
    version="1.0.0",
    description="Smart Learning Management System API untuk UAS Pemrograman Sisi Server",
    urls_namespace="smart_lms_api",
    auth=apiAuth,
)

api.add_router("/auth/", accounts_router)
api.add_router("/users/", users_router)
api.add_router("/courses/", courses_router)
api.add_router("/course-members/", members_router)
api.add_router("/course-contents/", contents_router)
api.add_router("/comments/", comments_router)
api.add_router("/dashboard/", dashboard_router)
api.add_router("/statistics/", statistics_router)
```

### Lampiran 3: File router.py (apps/courses/api/router.py)

```python
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from ninja import FilterSchema, Query, Router
from ninja.errors import HttpError

from apps.common.api.schemas import MessageSchema
from apps.common.api.utils import paginate_queryset, require_teacher
from apps.courses.models import Course
from apps.members.models import CourseMember

from .schemas import CourseCreateSchema, CourseDetailSchema, CourseListSchema, CourseOutSchema, CourseUpdateSchema, CourseFilterSchema


router = Router(tags=["Courses"])


def course_queryset():
    return Course.objects.select_related("teacher").annotate(
        content_count=Count("contents", distinct=True),
        member_count=Count("members", distinct=True),
        comment_count=Count("comments", distinct=True),
    )


def unique_slug(title, course_id=None):
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    qs = Course.objects.all()
    if course_id:
        qs = qs.exclude(id=course_id)
    while qs.filter(slug=slug).exists():
        counter += 1
        slug = f"{base_slug}-{counter}"
    return slug


@router.get("/", response=CourseListSchema, auth=None)
def list_courses(
    request,
    filters: CourseFilterSchema = Query(...),
    sort_by: str = Query("created_at", alias="sort_by"),
    page: int = 1,
    page_size: int = Query(5, alias="page_size"),
):
    queryset = course_queryset()
    queryset = filters.filter(queryset)
    
    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort_by == 'title_asc' or sort_by == 'name_asc':
        queryset = queryset.order_by('title')
    elif sort_by == 'title_desc' or sort_by == 'name_desc':
        queryset = queryset.order_by('-title')
    else:
        queryset = queryset.order_by('-created_at')
    
    return paginate_queryset(queryset, page, page_size)


@router.get("/{course_id}", response=CourseDetailSchema, auth=None)
def get_course(request, course_id: int):
    return get_object_or_404(course_queryset().prefetch_related("contents", "members"), id=course_id)


@router.post("/", response={201: CourseOutSchema})
@transaction.atomic
def create_course(request, payload: CourseCreateSchema):
    teacher = require_teacher(request)
    if payload.status not in Course.Status.values:
        raise HttpError(400, "Invalid course status.")
    course = Course.objects.create(
        title=payload.title,
        slug=unique_slug(payload.title),
        teacher=teacher,
        category=payload.category,
        price=payload.price,
        description=payload.description,
        status=payload.status,
    )
    CourseMember.objects.get_or_create(course=course, user=teacher, defaults={"role": CourseMember.Role.TEACHER})
    return 201, course_queryset().get(id=course.id)


@router.patch("/{course_id}", response=CourseOutSchema)
def update_course(request, course_id: int, payload: CourseUpdateSchema):
    teacher = require_teacher(request)
    course = get_object_or_404(Course, id=course_id)
    if course.teacher_id != teacher.id and teacher.role != "admin":
        raise HttpError(403, "You cannot edit another teacher course.")
    data = payload.dict(exclude_unset=True)
    if "status" in data and data["status"] not in Course.Status.values:
        raise HttpError(400, "Invalid course status.")
    if "title" in data:
        course.slug = unique_slug(data["title"], course.id)
    for field, value in data.items():
        setattr(course, field, value)
    course.save()
    return course_queryset().get(id=course.id)


@router.delete("/{course_id}", response=MessageSchema)
def delete_course(request, course_id: int):
    teacher = require_teacher(request)
    course = get_object_or_404(Course, id=course_id)
    if course.teacher_id != teacher.id and teacher.role != "admin":
        raise HttpError(403, "You cannot delete another teacher course.")
    course.delete()
    return {"message": "Course deleted successfully."}
```

### Lampiran 4: File middleware.py (apps/common/middleware.py)

```python
import time

from django.core.cache import cache
from django.http import JsonResponse


class ApiRateLimitMiddleware:
    window_seconds = 60
    anonymous_limit = 10
    authenticated_limit = 100
    login_limit = 5

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/v1/"):
            response = self.rate_limit(request)
            if response:
                return response
        return self.get_response(request)

    def rate_limit(self, request):
        now = int(time.time())
        window = now // self.window_seconds
        identity = self.identity(request)
        limit = self.login_limit if request.path == "/api/v1/auth/login" else self.request_limit(request)
        cache_key = f"throttle:{request.path}:{identity}:{window}"
        count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, count, timeout=self.window_seconds)
        if count > limit:
            return JsonResponse(
                {"detail": "Request was throttled. Please try again later."},
                status=429,
                headers={"Retry-After": str(self.window_seconds)},
            )
        return None

    def request_limit(self, request):
        return self.authenticated_limit if request.headers.get("Authorization") else self.anonymous_limit

    def identity(self, request):
        auth = request.headers.get("Authorization")
        if auth:
            return f"auth:{auth[-24:]}"
        return f"anon:{request.META.get('REMOTE_ADDR', 'unknown')}"
```

### Lampiran 5: File seed_data.py (apps/accounts/management/commands/seed_data.py)

```python
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

        self.stdout.write("Clearing existing data...")
        Comment.objects.all().delete()
        CourseContent.objects.all().delete()
        CourseMember.objects.all().delete()
        Enrollment.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Creating admin user...")
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@smartlms.com",
            password="admin123",
            role=User.Role.ADMIN,
            first_name="Smart",
            last_name="Admin",
        )

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

            CourseMember.objects.get_or_create(
                course=course,
                user=course.teacher,
                defaults={"role": CourseMember.Role.TEACHER},
            )

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
```

### Lampiran 6: File requirements.txt

```
Django>=5.0,<6.0
django-ninja>=1.1,<2.0
django-ninja-simple-jwt>=0.6,<1.0
psycopg2-binary>=2.9,<3.0
gunicorn>=22.0,<24.0
Pillow>=10.0,<12.0
PyJWT>=2.8,<3.0
python-dotenv>=1.0,<2.0
whitenoise
```

---

**Demikian Laporan Ujian Akhir Semester mata kuliah Pemrograman Sisi Server ini dibuat. Semoga dapat bermanfaat.**
