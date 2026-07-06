from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from apps.common.api.schemas import MessageSchema
from apps.common.api.utils import require_authenticated, require_teacher
from apps.courses.models import Course
from apps.members.models import CourseMember, Enrollment

from .schemas import CourseMemberSchema, EnrollmentSchema


router = Router(tags=["Course Members"])


@router.post("/enroll/{course_id}", response={201: EnrollmentSchema})
@transaction.atomic
def enroll_course(request, course_id: int):
    """
    Enroll the authenticated student into a course.

    Example request: POST /api/v1/course-members/enroll/1
    Example response: {"id": 1, "course_id": 1, "is_active": true}
    Status code: 201
    """
    user = require_authenticated(request)
    if user.role != "student":
        raise HttpError(403, "Only students can enroll.")
    course = get_object_or_404(Course, id=course_id)
    if Enrollment.objects.filter(course=course, student=user, is_active=True).exists():
        raise HttpError(400, "You are already enrolled in this course.")
    enrollment, _ = Enrollment.objects.update_or_create(
        course=course,
        student=user,
        defaults={"is_active": True},
    )
    CourseMember.objects.update_or_create(
        course=course,
        user=user,
        defaults={"role": CourseMember.Role.STUDENT},
    )
    return 201, enrollment


@router.post("/leave/{course_id}", response=MessageSchema)
@transaction.atomic
def leave_course(request, course_id: int):
    """
    Leave a course as authenticated student.

    Example request: POST /api/v1/course-members/leave/1
    Example response: {"message": "You have left the course."}
    Status code: 200
    """
    user = require_authenticated(request)
    updated = Enrollment.objects.filter(course_id=course_id, student=user, is_active=True).update(is_active=False)
    CourseMember.objects.filter(course_id=course_id, user=user, role=CourseMember.Role.STUDENT).delete()
    if not updated:
        raise HttpError(404, "Active enrollment not found.")
    return {"message": "You have left the course."}


@router.get("/course/{course_id}", response=list[CourseMemberSchema])
def list_members(request, course_id: int):
    """
    List course members. Teacher owner is required.

    Example request: GET /api/v1/course-members/course/1
    Example response: [{"id": 1, "username": "student01", "role": "student"}]
    Status code: 200
    """
    user = require_teacher(request)
    course = get_object_or_404(Course, id=course_id)
    if course.teacher_id != user.id and user.role != "admin":
        raise HttpError(403, "You cannot view members for another teacher course.")
    return CourseMember.objects.select_related("user", "course").filter(course=course)
