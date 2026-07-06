from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router

from apps.common.api.utils import require_authenticated

from .schemas import UserSchema, UserUpdateSchema


router = Router(tags=["Users"])
User = get_user_model()


@router.get("/", response=list[UserSchema])
def list_users(request):
    """
    List users for admin and dashboard needs.

    Example request: GET /api/v1/users/
    Example response: [{"id": 1, "username": "teacher01", "role": "teacher"}]
    Status code: 200
    """
    require_authenticated(request)
    return User.objects.order_by("username")


@router.get("/{user_id}", response=UserSchema)
def get_user(request, user_id: int):
    """
    Get a user profile by ID.

    Example request: GET /api/v1/users/1
    Example response: {"id": 1, "username": "student01", "role": "student"}
    Status code: 200
    """
    require_authenticated(request)
    return get_object_or_404(User, id=user_id)


@router.patch("/{user_id}", response=UserSchema)
def update_user(request, user_id: int, payload: UserUpdateSchema):
    """
    Update a user profile. The user can update only their own profile unless admin.

    Example request: {"bio": "Learning Django"}
    Example response: {"id": 1, "bio": "Learning Django"}
    Status code: 200
    """
    requester = require_authenticated(request)
    user = get_object_or_404(User, id=user_id)
    if requester.id != user.id and requester.role != "admin":
        from ninja.errors import HttpError

        raise HttpError(403, "You can only update your own profile.")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(user, field, value)
    user.save()
    return user
