# 📚 SmartLMS - Sistem Manajemen Pembelajaran Digital (UAS Backend)

## 📋 Deskripsi Proyek

SmartLMS adalah aplikasi backend Sistem Manajemen Pembelajaran berbasis Django dan Django Ninja REST API. Proyek ini dibuat untuk keperluan Ujian Akhir Semester (UAS) mata kuliah Pemrograman Server Side.

### Fitur Utama:
- 🔐 Autentikasi JWT per Role (Admin, Teacher, Student, Guest)
- 📊 Desain Database & Model yang Terstruktur
- 🚀 REST API dengan Django Ninja
- ⚡ Throttling, Pagination, Filtering, Sorting
- 🧪 Unit Testing (41 Test Cases)
- 📖 Dokumentasi Swagger/OpenAPI
- 🎨 Frontend Modern dengan Bootstrap 5
- 📝 Management Command untuk Seeding Data

---

## 📁 Struktur Proyek

```
smartlms_uas/
├── appmongo/                 # Konfigurasi project utama
│   ├── __init__.py
│   ├── asgi.py
│   ├── frontend_urls.py      # URL routing frontend
│   ├── settings.py           # Settings project
│   ├── urls.py               # URL utama project
│   ├── views.py              # Views untuk frontend
│   └── wsgi.py
├── apps/                     # Aplikasi Django
│   ├── accounts/             # Manajemen User & Authentication
│   ├── comments/             # Komentar pada konten
│   ├── common/               # Utility umum & API helpers
│   ├── contents/             # Konten course (materi, video, file)
│   ├── courses/              # Manajemen Course
│   ├── dashboard/            # Dashboard admin/teacher/student
│   └── members/              # Keanggotaan course
├── static/                   # File static (CSS, JS, Images)
├── templates/                # Template HTML
├── manage.py                 # Django manage script
└── requirements.txt          # Dependencies project
```

---

## 1. 📊 Desain Database, Model & Schema

### Database & Model

Proyek ini menggunakan PostgreSQL sebagai database utama. Berikut adalah model yang ada:

#### 1.1 User Model (`apps/accounts/models.py`)
```python
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"
        GUEST = "GUEST", "Guest"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)
```

#### 1.2 Course Model (`apps/courses/models.py`)
```python
class Course(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### 1.3 CourseContent Model (`apps/contents/models.py`)
```python
class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="contents")
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcontents")
    order = models.IntegerField(default=1)
```

#### 1.4 CourseMember & Enrollment Model (`apps/members/models.py`)
```python
class CourseMember(models.Model):
    class Role(models.TextChoices):
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=10, choices=Role.choices)

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
```

#### 1.5 Comment Model (`apps/comments/models.py`)
```python
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comments")
    content = models.ForeignKey(CourseContent, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Pydantic Schemas

Proyek menggunakan Pydantic untuk validasi API request/response. Contoh schema:
```python
# apps/courses/api/schemas.py
class CourseOutSchema(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    teacher_username: str
    status: str
```

---

## 2. 🚀 API Endpoints

### Base URL: `/api/v1`

#### 2.1 Courses API (`/api/v1/courses/`)
| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| `GET` | `/` | Daftar semua course (dengan filter, sort, pagination) | No |
| `GET` | `/{course_id}` | Detail course | No |
| `POST` | `/` | Buat course baru | Teacher/Admin |
| `PATCH` | `/{course_id}` | Update course | Teacher/Admin |
| `DELETE` | `/{course_id}` | Hapus course | Teacher/Admin |

#### 2.2 Filter & Query Parameters
- `search`: Cari course berdasarkan title, description, atau teacher username
- `price_gte`: Harga minimum
- `price_lte`: Harga maksimum
- `sort_by`: Urutkan (created_at, price_asc, price_desc, title_asc/name_asc, title_desc/name_desc)
- `page`: Halaman (default: 1)
- `page_size`: Jumlah item per halaman (default: 5, max: 50)

#### 2.3 Contoh Request API
```bash
# Daftar course dengan filter dan sort
GET /api/v1/courses/?search=django&price_gte=0&price_lte=1000000&sort_by=price_asc&page=1&page_size=10
```

---

## 3. 🔐 Authentication & Authorization

### 3.1 JWT Authentication
Proyek menggunakan `ninja-simple-jwt` untuk autentikasi JWT.

#### Endpoint Auth:
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `POST` | `/api/v1/auth/login` | Login (mendapatkan access & refresh token) |
| `POST` | `/api/v1/auth/refresh` | Refresh access token |
| `POST` | `/api/v1/auth/logout` | Logout |

#### Contoh Login Request:
```json
POST /api/v1/auth/login
{
  "username": "admin",
  "password": "admin123"
}
```

#### Response:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3.2 Role-Based Authorization
- **Admin**: Semua akses (CRUD user, course, dll)
- **Teacher**: CRUD course sendiri, kelola konten
- **Student**: Lihat course, join course, akses konten course yang diikuti
- **Guest**: Hanya lihat daftar course yang dipublikasi

---

## 4. ⚡ Throttling, Pagination, Filtering

### 4.1 Throttling
Rate limiting diterapkan pada API untuk mencegah abuse.
- **Anon User**: 100 requests/hour
- **Authenticated User**: 1000 requests/hour

Jika melebihi batas, akan mendapat response:
```json
{
  "detail": "Request was throttled. Please try again later."
}
```

### 4.2 Pagination
Pagination diterapkan pada endpoint daftar data. Response format:
```json
{
  "count": 20,
  "page": 1,
  "page_size": 5,
  "results": [ ... ]
}
```

### 4.3 Filtering & Search
Filtering menggunakan `CourseFilterSchema` di `apps/courses/api/schemas.py`.
- Filter harga (`price_gte`, `price_lte`)
- Search multi-field (title, description, teacher username)

---

## 5. 🧪 Unit Testing

Proyek memiliki 41 unit test untuk menguji:
- Model
- Views
- API Endpoints
- Authentication
- Authorization

### Cara Menjalankan Test:
```bash
python manage.py test
```

### Contoh Test Case:
- Test membuat user dengan role berbeda
- Test membuat course baru (hanya teacher/admin)
- Test endpoint API dengan filter dan sort
- Test pagination berjalan dengan benar
- Test authorization (user tidak boleh mengedit course orang lain)

---

## 6. 📖 Dokumentasi API (Swagger/OpenAPI)

Dokumentasi API otomatis di-generate oleh Django Ninja dan tersedia di:
- **Swagger UI**: `/api/v1/docs` (user-friendly interface)
- **OpenAPI JSON**: `/api/v1/openapi.json` (untuk keperluan integrasi)

Fitur di Swagger UI:
- Lihat semua endpoint
- Test endpoint langsung dari browser
- Lihat schema request/response
- Lihat contoh request/response

---

## 7. 📮 Uji API dengan Postman

### 7.1 Setup Postman Collection
Anda bisa import Postman Collection dari file `SmartLMS.postman_collection.json` (jika tersedia) atau buat secara manual.

### 7.2 Langkah-langkah Uji:
1. **Login**: Pilih method `POST`, URL `/api/v1/auth/login`, masukkan username dan password
2. **Simpan Token**: Salin `access_token` dari response
3. **Gunakan Token**: Pada setiap request yang membutuhkan auth, tambahkan header `Authorization: Bearer <access_token>`
4. **Uji Endpoint**: Coba request ke `/api/v1/courses/` dengan berbagai parameter (search, filter, sort, pagination)

### 7.3 Contoh Postman Request:
1. **Daftar Course**: `GET /api/v1/courses/?sort_by=price_asc&page=1&page_size=10`
2. **Detail Course**: `GET /api/v1/courses/1`
3. **Buat Course (Teacher Only)**: `POST /api/v1/courses/` dengan body JSON sesuai schema
4. **Test Throttling**: Kirim request berulang-ulang sampai mendapat status 429

---

## 8. 🚀 Instalasi & Menjalankan Proyek

### 8.1 Requirement
- Python 3.8+
- PostgreSQL (atau SQLite untuk development)
- pip

### 8.2 Langkah Instalasi:
1. **Clone repository**:
   ```bash
   git clone <url-repository>
   cd smartlms_uas
   ```

2. **Buat virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Aktivasi virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Konfigurasi Database**:
   - Salin `appmongo/settings.py` dan sesuaikan `DATABASES` sesuai database Anda
   - Untuk SQLite, setting sudah default dan siap pakai

6. **Jalankan migrasi**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Seed data dummy**:
   ```bash
   python manage.py seed_data
   ```
   Ini akan membuat:
   - 8 users (1 admin, 2 teacher, 5 student)
   - 8 courses
   - 24 course contents
   - 18 enrollments & course members
   - 24 comments

8. **Buat superuser (opsional)**:
   ```bash
   python manage.py createsuperuser
   ```

9. **Jalankan server**:
   ```bash
   python manage.py runserver
   ```

10. **Akses aplikasi**:
    - Frontend: `http://localhost:8000/`
    - Admin Panel: `http://localhost:8000/admin/`
    - API Docs: `http://localhost:8000/api/v1/docs`

### 8.3 Credential Awal (Setelah Seeding):
| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Teacher | budi_guru | guru123 |
| Teacher | siti_guru | guru123 |
| Student | ali_siswa | siswa123 |
| Student | (lainnya) | siswa123 |

---

## 9. 🎨 Frontend

Frontend dibuat dengan Bootstrap 5 dan tema baby blue putih modern.

### Halaman Utama:
1. **Home (`/`)**: Halaman utama, daftar course populer, statistik singkat
2. **Courses (`/courses/`)**: Daftar semua course dengan filter, search, sort, pagination
3. **Course Detail (`/courses/<id>/`)**: Detail course, tombol join, daftar konten
4. **Course Content List (`/courses/<id>/contents/`)**: Daftar konten course
5. **Content Detail (`/contents/<id>/`)**: Detail konten, komentar
6. **My Courses (`/my-courses/`)**: Daftar course yang diikuti user (hanya authenticated)
7. **Dashboard (`/dashboard/`)**: Dashboard sesuai role (Admin/Teacher/Student)
8. **Login (`/accounts/login/`)**: Halaman login modern dengan icon biru
9. **Logout (`/accounts/logout/`)**: Logout dari akun

---

## 10. 📝 Management Commands

### `seed_data`
Membuat data dummy untuk testing:
```bash
python manage.py seed_data
```

### Perintah Django Lainnya:
- `python manage.py check`: Periksa konfigurasi project
- `python manage.py makemigrations`: Buat migrasi
- `python manage.py migrate`: Jalankan migrasi
- `python manage.py createsuperuser`: Buat superuser
- `python manage.py collectstatic`: Kumpulkan file static

---

## 11. 📚 Teknologi yang Digunakan

| Teknologi | Versi | Deskripsi |
|-----------|-------|-----------|
| Django | 4.2+ | Web Framework |
| Django Ninja | 0.22+ | REST API Framework |
| ninja-simple-jwt | 1.0+ | JWT Authentication untuk Ninja |
| Bootstrap | 5.3 | CSS Framework |
| PostgreSQL | 13+ | Database (opsional SQLite) |
| Python | 3.8+ | Bahasa Pemrograman |

---

## 12. 📌 Catatan Penting

- **Project Lock**: Perubahan harus seminimal mungkin, tidak boleh mengubah struktur project besar
- **Tema**: Baby blue putih, Bootstrap 5 modern
- **Field Name**: Gunakan `title` untuk Course/CourseContent (bukan `name`)
- **Foreign Key**: Gunakan relationship langsung (misal `content.course` bukan `content.course_id`)

---

## 📞 Kontak

Untuk pertanyaan atau bantuan, hubungi:
- Nama: [Nama Anda]
- NIM: [NIM Anda]
- Kelas: [Kelas Anda]

---

**Selamat Belajar dan Semoga Sukses! 🎉**

## 13. Deployment Production: Koyeb + Neon

### Hasil Audit Deployment

- Django: `Django>=5.0,<6.0`; Docker image menggunakan Python 3.12.
- Runtime lokal saat audit: Python 3.13.2.
- Entry point: `manage.py`; settings: `appmongo.settings`.
- WSGI: `appmongo.wsgi:application`; tidak ada `asgi.py` aktual.
- Database: PostgreSQL melalui `psycopg2-binary`, dengan Neon melalui `DATABASE_URL`.
- API: Django Ninja dan `django-ninja-simple-jwt`, bukan Django REST Framework.
- CORS: tidak ada konfigurasi atau dependency CORS.
- Upload/media: avatar, thumbnail course, dan attachment content.
- Celery, Redis, dan background worker: tidak digunakan.
- Static files: WhiteNoise dengan `CompressedManifestStaticFilesStorage`.

### Environment Variables Koyeb

Buat variables berikut di Koyeb. Isi rahasia melalui dashboard Koyeb atau secret manager, bukan di source code:

```text
DJANGO_SECRET_KEY=<random-secret>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<koyeb-domain>
DJANGO_CSRF_TRUSTED_ORIGINS=https://<koyeb-domain>
DATABASE_URL=<neon-connection-string>
RUN_MIGRATIONS=True
RUN_COLLECTSTATIC=True
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
DJANGO_SECURE_HSTS_PRELOAD=True
```

`DATABASE_URL` harus berupa connection string Neon lengkap. Jangan menaruh password, API key, atau connection string asli di GitHub. Gunakan pooled connection string Neon untuk aplikasi Koyeb.

### Build, Run, dan Migration

Gunakan Docker builder Koyeb; `Dockerfile` sudah memasang dependency, menjalankan `collectstatic`, dan memakai port yang diberikan Koyeb:

```bash
pip install -r requirements.txt
gunicorn appmongo.wsgi:application --bind 0.0.0.0:$PORT
python manage.py migrate --noinput
```

Entrypoint menjalankan migration dan collectstatic ketika `RUN_MIGRATIONS=True` dan `RUN_COLLECTSTATIC=True`. Jangan menjalankan `makemigrations` di production kecuali ada perubahan model yang disengaja.

### Deployment Koyeb dari GitHub

1. Review lalu push perubahan ke repository GitHub secara manual. Assistant tidak melakukan push atau deployment.
2. Di Koyeb, buat App baru dan pilih deployment dari GitHub.
3. Pilih repository, branch, dan Docker builder.
4. Tambahkan environment variables production di atas sebagai values/secrets.
5. Pastikan service memakai public port `8000`; aplikasi tetap bind ke `$PORT` yang diberikan Koyeb.
6. Deploy dan periksa logs sampai migration serta Gunicorn berhasil.

### Koneksi Neon

1. Buat project/database PostgreSQL di Neon.
2. Salin pooled connection string dari Neon.
3. Simpan sebagai secret `DATABASE_URL` di Koyeb.
4. Dengan `DJANGO_DEBUG=False`, konfigurasi mewajibkan SSL pada koneksi database.
5. Jalankan migration dan verifikasi tabel aplikasi.

Upload media tersimpan di filesystem container dan tidak persisten pada deployment stateless. Untuk production, gunakan object storage persisten sebelum mengandalkan upload pengguna.

### Testing Setelah Deployment

```bash
curl https://<koyeb-domain>/
curl https://<koyeb-domain>/api/v1/docs
curl https://<koyeb-domain>/api/v1/openapi.json
```

Lanjutkan dengan login JWT, request endpoint course, upload media, dan akses admin. Periksa juga service status, deployment logs Koyeb, serta koneksi database Neon.

## 14. Production VPS Deployment

For the supported Ubuntu VPS deployment, use Docker Compose with PostgreSQL, Gunicorn, WhiteNoise, and Nginx:

```text
Internet -> Nginx -> 127.0.0.1:8000 (SmartLMS/Gunicorn) -> PostgreSQL internal Docker network
```

The production Compose configuration:

- reads secrets and database credentials from an untracked `.env`;
- does not publish PostgreSQL to the host;
- uses a persistent named volume for PostgreSQL and media; static files are baked into the image;
- runs the web image as a non-root user;
- exposes `/health/` for container health checks;
- runs Gunicorn instead of Django `runserver`.

Create the environment file and deploy with:

```bash
cp .env.example .env
chmod 600 .env
docker compose config --quiet
docker compose build
docker compose up -d
docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py collectstatic --noinput
```

Set `DJANGO_DEBUG=False`, a long random `DJANGO_SECRET_KEY`, the real `DJANGO_ALLOWED_HOSTS`, HTTPS `DJANGO_CSRF_TRUSTED_ORIGINS`, and strong PostgreSQL variables in `.env`. Never commit `.env`.

See [DEPLOYMENT.md](DEPLOYMENT.md) for the complete VPS, Nginx, HTTPS, health check, update, and backup procedure.
