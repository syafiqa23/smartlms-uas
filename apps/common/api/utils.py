from django.core.paginator import EmptyPage, Paginator
from ninja.errors import HttpError


def require_authenticated(request):
    user = request.user
    if not user.is_authenticated:
        raise HttpError(401, "Authentication required.")
    return user


def require_teacher(request):
    user = require_authenticated(request)
    if user.role not in {"teacher", "admin"}:
        raise HttpError(403, "Teacher role required.")
    return user


def paginate_queryset(queryset, page=1, page_size=10):
    if page_size not in {5, 10, 20}:
        raise HttpError(400, "page_size must be 5, 10, or 20.")

    paginator = Paginator(queryset, page_size)
    try:
        items = list(paginator.page(page).object_list)
    except EmptyPage:
        items = []

    return {
        "count": paginator.count,
        "page": page,
        "page_size": page_size,
        "results": items,
    }
