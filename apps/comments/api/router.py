from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from apps.comments.models import Comment
from apps.common.api.schemas import MessageSchema
from apps.common.api.utils import require_authenticated
from apps.contents.models import CourseContent
from apps.courses.models import Course
from apps.members.models import Enrollment

from .schemas import CommentCreateSchema, CommentSchema, CommentUpdateSchema


router = Router(tags=["Comments"])


def validation_error_message(exc):
    if hasattr(exc, "message_dict"):
        return " ".join(
            f"{field}: {' '.join(str(message) for message in messages)}"
            for field, messages in exc.message_dict.items()
        )
    return " ".join(str(message) for message in exc.messages)


def ensure_can_comment(user, course):
    if course.teacher_id == user.id:
        return
    if not Enrollment.objects.filter(course=course, student=user, is_active=True).exists():
        raise HttpError(403, "You must enroll before commenting.")


@router.get("/", response=list[CommentSchema])
def list_comments(request, course_id: int | None = None, content_id: int | None = None):
    """
    List comments and replies.

    Example request: GET /api/v1/comments/?course_id=1
    Example response: [{"id": 1, "text": "Bagus", "parent_id": null}]
    Status code: 200
    """
    queryset = Comment.objects.select_related("user", "course", "content", "parent").prefetch_related("replies")
    if course_id:
        queryset = queryset.filter(course_id=course_id)
    if content_id:
        queryset = queryset.filter(content_id=content_id)
    return queryset


@router.post("/", response={201: CommentSchema})
@transaction.atomic
def create_comment(request, payload: CommentCreateSchema):
    """
    Create comment or nested reply. Enrollment is required for students.

    Example request: {"course_id": 1, "content_id": 1, "text": "Materinya jelas"}
    Example response: {"id": 1, "text": "Materinya jelas"}
    Status code: 201
    """
    user = require_authenticated(request)
    course = get_object_or_404(Course, id=payload.course_id)
    ensure_can_comment(user, course)
    content = None
    parent = None
    if payload.content_id:
        content = get_object_or_404(CourseContent, id=payload.content_id)
        if content.course_id != course.id:
            raise HttpError(400, "Content must belong to the selected course.")
    if payload.parent_id:
        parent = get_object_or_404(Comment, id=payload.parent_id)
        if parent.course_id != course.id:
            raise HttpError(400, "Parent comment must belong to the selected course.")
    comment = Comment(course=course, content=content, user=user, parent=parent, text=payload.text)
    try:
        comment.full_clean()
    except ValidationError as exc:
        raise HttpError(400, validation_error_message(exc))
    comment.save()
    return 201, comment


@router.patch("/{comment_id}", response=CommentSchema)
def update_comment(request, comment_id: int, payload: CommentUpdateSchema):
    """
    Update own comment.

    Example request: {"text": "Materinya sangat jelas"}
    Example response: {"id": 1, "text": "Materinya sangat jelas"}
    Status code: 200
    """
    user = require_authenticated(request)
    comment = get_object_or_404(Comment.objects.select_related("user"), id=comment_id)
    if comment.user_id != user.id and user.role != "admin":
        raise HttpError(403, "You can only edit your own comment.")
    comment.text = payload.text
    try:
        comment.full_clean()
    except ValidationError as exc:
        raise HttpError(400, validation_error_message(exc))
    comment.save(update_fields=["text", "updated_at"])
    return comment


@router.delete("/{comment_id}", response=MessageSchema)
def delete_comment(request, comment_id: int):
    """
    Delete own comment.

    Example request: DELETE /api/v1/comments/1
    Example response: {"message": "Comment deleted successfully."}
    Status code: 200
    """
    user = require_authenticated(request)
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user_id != user.id and user.role != "admin":
        raise HttpError(403, "You can only delete your own comment.")
    comment.delete()
    return {"message": "Comment deleted successfully."}
