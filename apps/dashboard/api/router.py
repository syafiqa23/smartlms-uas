from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDate
from ninja import Router

from apps.comments.models import Comment
from apps.common.api.utils import require_authenticated
from apps.contents.models import CourseContent
from apps.courses.models import Course
from apps.members.models import Enrollment

from .schemas import DashboardSchema


router = Router(tags=["Dashboard"])
User = get_user_model()


def chart_by_date(queryset, date_field):
    return [
        {"label": str(item["day"]), "value": item["total"]}
        for item in queryset.annotate(day=TruncDate(date_field)).values("day").annotate(total=Count("id")).order_by("day")
    ]


def user_role_chart():
    return [
        {"label": item["role"], "value": item["value"]}
        for item in User.objects.values("role").annotate(value=Count("id")).order_by("role")
    ]


@router.get("/", response=DashboardSchema, operation_id="dashboard_summary")
def dashboard_summary(request):
    """
    Return dashboard counters, charts, and recent activity.

    Example request: GET /api/v1/dashboard/
    Example response: {"total_course": 3, "total_student": 10, "total_teacher": 2}
    Status code: 200
    """
    require_authenticated(request)
    recent_courses = Course.objects.select_related("teacher").order_by("-created_at")[:5]
    recent_comments = Comment.objects.select_related("user", "course").order_by("-created_at")[:5]
    recent_activity = [
        {"type": "course", "label": course.title, "created_at": course.created_at.isoformat()}
        for course in recent_courses
    ] + [
        {"type": "comment", "label": f"{comment.user.username} on {comment.course.title}", "created_at": comment.created_at.isoformat()}
        for comment in recent_comments
    ]
    recent_activity = sorted(recent_activity, key=lambda item: item["created_at"], reverse=True)[:10]

    return {
        "total_course": Course.objects.count(),
        "total_student": User.objects.filter(role="student").count(),
        "total_teacher": User.objects.filter(role="teacher").count(),
        "total_comment": Comment.objects.count(),
        "total_content": CourseContent.objects.count(),
        "course_chart": chart_by_date(Course.objects.all(), "created_at"),
        "user_chart": user_role_chart(),
        "enrollment_chart": chart_by_date(Enrollment.objects.all(), "enrolled_at"),
        "recent_activity": recent_activity,
    }
