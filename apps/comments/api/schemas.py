from datetime import datetime
from typing import Optional

from ninja import Schema
from pydantic import Field


class CommentCreateSchema(Schema):
    course_id: int
    content_id: Optional[int] = None
    parent_id: Optional[int] = None
    text: str = Field(..., min_length=3)


class CommentUpdateSchema(Schema):
    text: str = Field(..., min_length=3)


class CommentSchema(Schema):
    id: int
    course_id: int
    content_id: Optional[int] = None
    user_id: int
    username: str
    parent_id: Optional[int] = None
    text: str
    created_at: datetime

    @staticmethod
    def resolve_username(obj):
        return obj.user.username
