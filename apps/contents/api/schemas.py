from datetime import datetime
from typing import Optional

from ninja import Schema
from pydantic import Field


class CourseContentCreateSchema(Schema):
    course_id: int
    title: str = Field(..., min_length=5)
    video_url: str = ""
    description: str = ""
    order: int = Field(1, ge=1)


class CourseContentUpdateSchema(Schema):
    title: Optional[str] = Field(None, min_length=5)
    video_url: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = Field(None, ge=1)


class CourseContentSchema(Schema):
    id: int
    course_id: int
    title: str
    video_url: str
    attachment: Optional[str] = None
    description: str
    order: int
    created_at: datetime

    @staticmethod
    def resolve_attachment(obj):
        return obj.attachment.url if obj.attachment else None
