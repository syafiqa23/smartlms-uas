from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from ninja import Router
from ninja.errors import HttpError
from jwt import PyJWTError
from ninja_simple_jwt.jwt.token_operations import (
    get_access_token_for_user,
    get_access_token_from_refresh_token,
    get_refresh_token_for_user,
)

from apps.common.api.schemas import MessageSchema
from apps.common.api.utils import require_authenticated

from .schemas import (
    AccessTokenSchema,
    ChangePasswordSchema,
    LoginSchema,
    RefreshTokenSchema,
    TokenPairSchema,
    UserRegisterSchema,
    UserSchema,
    UserUpdateSchema,
)


router = Router(tags=["Authentication"])
User = get_user_model()


def validation_error_message(exc):
    return " ".join(str(message) for message in exc.messages)


@router.post("/register", response={201: UserSchema}, auth=None)
@transaction.atomic
def register(request, payload: UserRegisterSchema):
    """
    Register a new Smart LMS user.

    Example request: {"username": "student01", "email": "student@example.com", "password": "password123", "role": "student"}
    Example response: {"id": 1, "username": "student01", "email": "student@example.com", "role": "student"}
    Status code: 201
    """
    if payload.role not in {"student", "teacher"}:
        raise HttpError(400, "Role must be student or teacher.")
    try:
        validate_email(payload.email)
    except ValidationError:
        raise HttpError(400, "Email is invalid.")
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "Username already exists.")
    if User.objects.filter(email=payload.email).exists():
        raise HttpError(400, "Email already exists.")

    try:
        validate_password(payload.password)
    except ValidationError as exc:
        raise HttpError(400, validation_error_message(exc))
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,
        role=payload.role,
    )
    return 201, user


@router.post("/login", response=TokenPairSchema, auth=None)
def login(request, payload: LoginSchema):
    """
    Login with username and password to receive JWT access and refresh tokens.

    Example request: {"username": "student01", "password": "UasSmart98765"}
    Example response: {"access": "jwt-access-token", "refresh": "jwt-refresh-token", "token_type": "Bearer"}
    Status code: 200
    """
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is None:
        raise HttpError(401, "Invalid username or password.")
    if not user.is_active:
        raise HttpError(403, "User account is inactive.")
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    refresh_token, _ = get_refresh_token_for_user(user)
    access_token, _ = get_access_token_for_user(user)
    return {"access": access_token, "refresh": refresh_token, "token_type": "Bearer"}


@router.post("/refresh", response=AccessTokenSchema, auth=None)
def refresh_token(request, payload: RefreshTokenSchema):
    """
    Refresh an access token using a valid refresh token.

    Example request: {"refresh": "jwt-refresh-token"}
    Example response: {"access": "new-jwt-access-token", "token_type": "Bearer"}
    Status code: 200
    """
    try:
        access_token, _ = get_access_token_from_refresh_token(payload.refresh)
    except PyJWTError:
        raise HttpError(401, "Invalid or expired refresh token.")
    return {"access": access_token, "token_type": "Bearer"}


@router.post("/logout", response=MessageSchema)
def logout(request):
    """
    Logout the authenticated user by instructing the client to discard tokens.

    Example request: POST /api/v1/auth/logout with Authorization: Bearer token
    Example response: {"message": "Logout successful. Please discard the access and refresh tokens."}
    Status code: 200
    """
    require_authenticated(request)
    return {"message": "Logout successful. Please discard the access and refresh tokens."}


@router.get("/me", response=UserSchema)
def me(request):
    """
    Return the authenticated user profile.

    Example request: GET /api/v1/auth/me
    Example response: {"id": 1, "username": "teacher01", "role": "teacher"}
    Status code: 200
    """
    return require_authenticated(request)


@router.patch("/me", response=UserSchema)
def update_me(request, payload: UserUpdateSchema):
    """
    Update the authenticated user profile.

    Example request: {"first_name": "Siti", "bio": "Backend learner"}
    Example response: {"id": 1, "username": "siti01", "bio": "Backend learner"}
    Status code: 200
    """
    user = require_authenticated(request)
    data = payload.dict(exclude_unset=True)
    if "role" in data and data["role"] not in {"student", "teacher"}:
        raise HttpError(400, "Role must be student or teacher.")
    for field, value in data.items():
        setattr(user, field, value)
    user.save()
    return user


@router.post("/change-password", response=MessageSchema)
def change_password(request, payload: ChangePasswordSchema):
    """
    Change password for the authenticated user.

    Example request: {"old_password": "password123", "new_password": "newpass123"}
    Example response: {"message": "Password updated successfully."}
    Status code: 200
    """
    user = require_authenticated(request)
    if not user.check_password(payload.old_password):
        raise HttpError(400, "Old password is incorrect.")
    try:
        validate_password(payload.new_password, user)
    except ValidationError as exc:
        raise HttpError(400, validation_error_message(exc))
    user.set_password(payload.new_password)
    user.save(update_fields=["password"])
    return {"message": "Password updated successfully."}
