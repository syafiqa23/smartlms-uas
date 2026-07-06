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
    """
    List courses with search, filtering, sorting, and pagination.

    Example request: GET /api/v1/courses/?search=django&page=1&page_size=5&sort_by=price_desc
    Example response: {"count": 1, "page": 1, "page_size": 5, "results": []}
    Status code: 200
    """
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


@router.get("/{course_id}", response=CourseDetailSchema, auth=None)
def get_course(request, course_id: int):
    """
    Get course detail.

    Example request: GET /api/v1/courses/1
    Example response: {"id": 1, "title": "Django Backend Dasar"}
    Status code: 200
    """
    return get_object_or_404(course_queryset().prefetch_related("contents", "members"), id=course_id)


@router.post("/", response={201: CourseOutSchema})
@transaction.atomic
def create_course(request, payload: CourseCreateSchema):
    """
    Create a new course. Teacher role is required.

    Example request: {"title": "Django Backend Dasar", "category": "Backend", "price": 150000, "description": "Belajar Django"}
    Example response: {"id": 1, "title": "Django Backend Dasar", "status": "draft"}
    Status code: 201
    """
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
    """
    Update a course owned by the authenticated teacher.

    Example request: {"price": 200000, "status": "published"}
    Example response: {"id": 1, "price": 200000, "status": "published"}
    Status code: 200
    """
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
    """
    Delete a course owned by the authenticated teacher.

    Example request: DELETE /api/v1/courses/1
    Example response: {"message": "Course deleted successfully."}
    Status code: 200
    """
    teacher = require_teacher(request)
    course = get_object_or_404(Course, id=course_id)
    if course.teacher_id != teacher.id and teacher.role != "admin":
        raise HttpError(403, "You cannot delete another teacher course.")
    course.delete()
    return {"message": "Course deleted successfully."}
