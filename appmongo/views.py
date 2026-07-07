import csv
import io
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.comments.models import Comment
from apps.contents.forms import CourseContentForm
from apps.contents.models import CourseContent
from apps.courses.forms import CourseForm
from apps.courses.models import Course
from apps.members.models import CourseMember, Enrollment

User = get_user_model()


def home(request):
    total_courses = Course.objects.count()
    total_users = User.objects.count()
    total_comments = Comment.objects.count()
    popular_courses = Course.objects.annotate(
        member_count=Count("members", distinct=True)
    ).order_by("-member_count")[:5]

    return render(
        request,
        "dashboard/home.html",
        {
            "total_courses": total_courses,
            "total_users": total_users,
            "total_comments": total_comments,
            "popular_courses": popular_courses,
            "active": "dashboard",
        },
    )


@login_required
def dashboard_page(request):
    user = request.user
    stats = {}
    user_courses = CourseMember.objects.select_related("course").filter(user=user)

    if user.role == User.Role.ADMIN:
        stats = {
            "total_users": User.objects.count(),
            "total_teachers": User.objects.filter(role=User.Role.TEACHER).count(),
            "total_students": User.objects.filter(role=User.Role.STUDENT).count(),
            "total_courses": Course.objects.count(),
            "total_contents": CourseContent.objects.count(),
            "total_enrollments": Enrollment.objects.count(),
            "total_comments": Comment.objects.count(),
        }
    elif user.role == User.Role.TEACHER:
        teacher_courses = Course.objects.filter(teacher=user)
        stats = {
            "total_courses": teacher_courses.count(),
            "total_students": CourseMember.objects.filter(
                course__in=teacher_courses, role=CourseMember.Role.STUDENT
            ).count(),
            "total_contents": CourseContent.objects.filter(course__in=teacher_courses).count(),
            "total_comments": Comment.objects.filter(course__in=teacher_courses).count(),
        }
    else:  # STUDENT
        student_enrollments = Enrollment.objects.filter(student=user, is_active=True)
        student_courses = [e.course for e in student_enrollments]
        stats = {
            "total_courses": student_enrollments.count(),
            "total_comments": Comment.objects.filter(user=user).count(),
            "active_courses": student_enrollments.count(),
        }

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "stats": stats,
            "courses": user_courses,
            "user_role": user.role,
            "active": "dashboard",
        },
    )


def course_list(request):
    # Base queryset with member count annotation
    courses = Course.objects.filter(status=Course.Status.PUBLISHED).annotate(
        member_count=Count("members", distinct=True),
        content_count=Count("contents", distinct=True)
    )
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(teacher__username__icontains=search_query)
        )
    
    # Price filtering
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        courses = courses.filter(price__gte=price_min)
    if price_max:
        courses = courses.filter(price__lte=price_max)
    
    # Sorting functionality
    sort_by = request.GET.get('sort_by', 'created_at')
    if sort_by == 'price_asc':
        courses = courses.order_by('price')
    elif sort_by == 'price_desc':
        courses = courses.order_by('-price')
    elif sort_by == 'name_asc':
        courses = courses.order_by('title')
    elif sort_by == 'name_desc':
        courses = courses.order_by('-title')
    else:  # Default: created_at
        courses = courses.order_by('-created_at')
    
    # Per page
    per_page = request.GET.get('per_page', '5')
    try:
        per_page_int = int(per_page)
        if per_page_int not in [5, 10, 20, 50]:
            per_page_int = 5
    except (ValueError, TypeError):
        per_page_int = 5
    
    # Pagination
    paginator = Paginator(courses, per_page_int)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        "courses/course_list.html",
        {
            "page_obj": page_obj,
            "courses": page_obj.object_list,
            "search_query": search_query,
            "sort_by": sort_by,
            "price_min": price_min,
            "price_max": price_max,
            "per_page": per_page_int,
            "active": "courses",
        },
    )


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    contents = course.contents.all().order_by("order")

    is_member = False
    if request.user.is_authenticated:
        is_member = CourseMember.objects.filter(course=course, user=request.user).exists()

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "contents": contents,
            "is_member": is_member,
            "active": "courses",
        },
    )


@login_required
def join_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Validasi: Teacher tidak bisa join course sendiri
    if course.teacher == request.user:
        messages.error(request, "Anda adalah pengajar kursus ini, tidak bisa bergabung sebagai siswa.")
        return redirect("course_detail", course_id=course.id)
    
    # Cek apakah sudah join
    is_member = CourseMember.objects.filter(course=course, user=request.user).exists()
    if is_member:
        messages.warning(request, "Anda sudah terdaftar di kursus ini.")
        return redirect("course_detail", course_id=course.id)
    
    # Hanya student yang bisa join
    if request.user.role == User.Role.STUDENT:
        Enrollment.objects.update_or_create(
            course=course,
            student=request.user,
            defaults={"is_active": True},
        )
        CourseMember.objects.update_or_create(
            course=course,
            user=request.user,
            defaults={"role": CourseMember.Role.STUDENT},
        )
        messages.success(request, f"Berhasil bergabung dengan kursus {course.title}!")
    
    return redirect("course_detail", course_id=course.id)


def course_content_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    contents = course.contents.all().order_by("order")

    can_view = False
    if request.user.is_authenticated:
        can_view = (course.teacher == request.user) or CourseMember.objects.filter(
            course=course, user=request.user
        ).exists()

    return render(
        request,
        "courses/course_content_list.html",
        {
            "course": course,
            "contents": contents,
            "can_view": can_view,
            "active": "courses",
        },
    )


def course_content_detail(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id)
    course = content.course
    comments = content.comments.all().order_by("created_at")

    can_view = False
    can_assist = False
    if request.user.is_authenticated:
        can_view = (course.teacher == request.user) or CourseMember.objects.filter(
            course=course, user=request.user
        ).exists()
        can_assist = course.teacher == request.user or request.user.role == User.Role.ADMIN

    return render(
        request,
        "courses/course_content_detail.html",
        {
            "content": content,
            "comments": comments,
            "can_view": can_view,
            "can_assist": can_assist,
            "active": "courses",
        },
    )


@login_required
def add_comment(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id)
    course = content.course

    is_enrolled = CourseMember.objects.filter(course=course, user=request.user).exists() or (
        course.teacher == request.user
    )
    if not is_enrolled:
        return redirect("course_content_detail", content_id=content.id)

    if request.method == "POST":
        text = request.POST.get("comment", "").strip()
        if text:
            Comment.objects.create(
                course=course,
                content=content,
                user=request.user,
                text=text,
            )
            messages.success(request, "Komentar berhasil ditambahkan!")
            return redirect("course_content_detail", content_id=content.id)
    
    return render(
        request,
        "comments/add_comment.html",
        {
            "content": content,
            "active": "courses",
        },
    )


@login_required
def my_courses(request):
    memberships = CourseMember.objects.select_related("course", "course__teacher").filter(user=request.user)
    return render(
        request,
        "members/my_courses.html",
        {
            "memberships": memberships,
            "active": "my_courses",
        },
    )


@login_required
def edit_content(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id)
    course = content.course
    
    # Hanya teacher atau admin yang bisa edit
    if not (request.user == course.teacher or request.user.role == User.Role.ADMIN):
        messages.error(request, "Anda tidak memiliki izin untuk mengedit konten ini.")
        return redirect("course_content_detail", content_id=content.id)
    
    if request.method == "POST":
        form = CourseContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, "Konten berhasil diperbarui!")
            return redirect("course_content_detail", content_id=content.id)
    else:
        form = CourseContentForm(instance=content)
    
    return render(
        request,
        "contents/edit_content.html",
        {
            "form": form,
            "content": content,
            "active": "courses",
        },
    )


@login_required
def create_course(request):
    if request.user.role != User.Role.TEACHER:
        messages.error(request, "Anda tidak memiliki izin untuk membuat kursus.")
        return redirect("course_list")
    
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            # Add teacher as member
            CourseMember.objects.get_or_create(
                course=course,
                user=request.user,
                defaults={"role": CourseMember.Role.TEACHER},
            )
            messages.success(request, "Kursus berhasil dibuat!")
            return redirect("course_detail", course_id=course.id)
    else:
        form = CourseForm()
    
    return render(
        request,
        "courses/create_course.html",
        {"form": form, "active": "courses"},
    )


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if not (request.user == course.teacher or request.user.role == User.Role.ADMIN):
        messages.error(request, "Anda tidak memiliki izin untuk mengedit kursus ini.")
        return redirect("course_detail", course_id=course.id)
    
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Kursus berhasil diperbarui!")
            return redirect("course_detail", course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    return render(
        request,
        "courses/edit_course.html",
        {"form": form, "course": course, "active": "courses"},
    )


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if not (request.user == course.teacher or request.user.role == User.Role.ADMIN):
        messages.error(request, "Anda tidak memiliki izin untuk menghapus kursus ini.")
        return redirect("course_detail", course_id=course.id)
    
    if request.method == "POST":
        course.delete()
        messages.success(request, "Kursus berhasil dihapus!")
        return redirect("course_list")
    
    return render(
        request,
        "courses/delete_course.html",
        {"course": course, "active": "courses"},
    )


@login_required
def add_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if not (request.user == course.teacher or request.user.role == User.Role.ADMIN):
        messages.error(request, "Anda tidak memiliki izin untuk menambah konten.")
        return redirect("course_content_list", course_id=course.id)
    
    if request.method == "POST":
        form = CourseContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.course = course
            content.save()
            messages.success(request, "Konten berhasil ditambahkan!")
            return redirect("course_content_list", course_id=course.id)
    else:
        form = CourseContentForm()
    
    return render(
        request,
        "contents/add_content.html",
        {"form": form, "course": course, "active": "courses"},
    )


@login_required
def delete_content(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id)
    course = content.course
    
    if not (request.user == course.teacher or request.user.role == User.Role.ADMIN):
        messages.error(request, "Anda tidak memiliki izin untuk menghapus konten ini.")
        return redirect("course_content_detail", content_id=content.id)
    
    if request.method == "POST":
        content.delete()
        messages.success(request, "Konten berhasil dihapus!")
        return redirect("course_content_list", course_id=course.id)
    
    return render(
        request,
        "contents/delete_content.html",
        {"content": content, "course": course, "active": "courses"},
    )


@login_required
def download_csv_template(request):
    if request.user.role != User.Role.TEACHER:
        messages.error(request, "Anda tidak memiliki izin.")
        return redirect("dashboard")
    
    # Create CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header row
    writer.writerow(["title", "category", "price", "description", "status"])
    
    # Write example data
    writer.writerow(["Pemrograman Python Dasar", "Programming", 50000, "Kursus dasar pemrograman Python untuk pemula", "published"])
    
    # Create response
    output.seek(0)
    response = HttpResponse(output, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="template_kursus.csv"'
    
    return response


@login_required
def import_csv(request):
    if request.user.role != User.Role.TEACHER:
        messages.error(request, "Anda tidak memiliki izin.")
        return redirect("dashboard")
    
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        
        if not csv_file:
            messages.error(request, "Silakan pilih file CSV terlebih dahulu.")
            return redirect("import_csv")
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "File harus berformat CSV.")
            return redirect("import_csv")
        
        try:
            # Read CSV file
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            
            for row in reader:
                try:
                    # Always use request.user as teacher
                    teacher = request.user
                    
                    # Create course
                    course = Course.objects.create(
                        title=row.get("title", ""),
                        category=row.get("category", ""),
                        price=int(row.get("price", 0)),
                        description=row.get("description", ""),
                        status=row.get("status", "draft"),
                        teacher=teacher
                    )
                    
                    # Add teacher as member
                    CourseMember.objects.get_or_create(
                        course=course,
                        user=teacher,
                        defaults={"role": CourseMember.Role.TEACHER}
                    )
                    
                    success_count += 1
                except Exception:
                    error_count += 1
            
            if success_count > 0:
                messages.success(request, f"Berhasil mengimport {success_count} kursus!")
            if error_count > 0:
                messages.warning(request, f"Gagal mengimport {error_count} baris data.")
            
            return redirect("course_list")
        
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan saat mengimport file: {str(e)}")
            return redirect("import_csv")
    
    return render(
        request,
        "courses/import_csv.html",
        {"active": "dashboard"},
    )
