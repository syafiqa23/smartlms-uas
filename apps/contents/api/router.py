from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from apps.common.api.schemas import MessageSchema
from apps.common.api.utils import require_teacher
from apps.contents.models import CourseContent
from apps.courses.models import Course

from .schemas import CourseContentCreateSchema, CourseContentSchema, CourseContentUpdateSchema


router = Router(tags=["Course Contents"])


def ensure_course_teacher(request, course):
    user = require_teacher(request)
    if course.teacher_id != user.id and user.role != "admin":
        raise HttpError(403, "You cannot manage content for another teacher course.")
    return user


@router.get("/", response=list[CourseContentSchema])
def list_contents(request, course_id: int | None = None):
    """
    List course contents.

    Example request: GET /api/v1/course-contents/?course_id=1
    Example response: [{"id": 1, "title": "Intro", "order": 1}]
    Status code: 200
    """
    queryset = CourseContent.objects.select_related("course").order_by("course_id", "order")
    if course_id:
        queryset = queryset.filter(course_id=course_id)
    return queryset


@router.post("/", response={201: CourseContentSchema})
@transaction.atomic
def create_content(request, payload: CourseContentCreateSchema):
    """
    Create course content. Teacher owner is required.

    Example request: {"course_id": 1, "title": "Intro Django", "order": 1}
    Example response: {"id": 1, "course_id": 1, "title": "Intro Django"}
    Status code: 201
    """
    course = get_object_or_404(Course, id=payload.course_id)
    ensure_course_teacher(request, course)
    try:
        content = CourseContent.objects.create(**payload.dict())
    except IntegrityError:
        raise HttpError(400, "Content order already exists for this course.")
    return 201, content


@router.get("/{content_id}", response=CourseContentSchema)
def get_content(request, content_id: int):
    """
    Get course content detail.

    Example request: GET /api/v1/course-contents/1
    Example response: {"id": 1, "title": "Intro Django"}
    Status code: 200
    """
    return get_object_or_404(CourseContent.objects.select_related("course"), id=content_id)


@router.patch("/{content_id}", response=CourseContentSchema)
def update_content(request, content_id: int, payload: CourseContentUpdateSchema):
    """
    Update course content owned by teacher.

    Example request: {"title": "Intro Django ORM"}
    Example response: {"id": 1, "title": "Intro Django ORM"}
    Status code: 200
    """
    content = get_object_or_404(CourseContent.objects.select_related("course"), id=content_id)
    ensure_course_teacher(request, content.course)
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(content, field, value)
    try:
        content.save()
    except IntegrityError:
        raise HttpError(400, "Content order already exists for this course.")
    return content


@router.delete("/{content_id}", response=MessageSchema)
def delete_content(request, content_id: int):
    """
    Delete course content owned by teacher.

    Example request: DELETE /api/v1/course-contents/1
    Example response: {"message": "Content deleted successfully."}
    Status code: 200
    """
    content = get_object_or_404(CourseContent.objects.select_related("course"), id=content_id)
    ensure_course_teacher(request, content.course)
    content.delete()
    return {"message": "Content deleted successfully."}
