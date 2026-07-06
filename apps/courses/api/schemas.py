from datetime import datetime
from decimal import Decimal
from typing import Optional

from ninja import FilterSchema, Schema
from pydantic import Field


class CourseCreateSchema(Schema):
    title: str = Field(..., min_length=5, examples=["Django Backend Dasar"])
    category: str = Field(..., examples=["Backend"])
    price: Decimal = Field(0, ge=0, examples=[150000])
    description: str = Field(..., examples=["Belajar Django ORM dan REST API."])
    status: str = Field("draft", examples=["published"])


class CourseUpdateSchema(Schema):
    title: Optional[str] = Field(None, min_length=5)
    category: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = None
    status: Optional[str] = None


class CourseOutSchema(Schema):
    id: int
    title: str
    slug: str
    teacher_id: int
    teacher_username: str
    category: str
    price: Decimal
    description: str
    status: str
    thumbnail: Optional[str] = None
    created_at: datetime
    content_count: int = 0
    member_count: int = 0
    comment_count: int = 0

    @staticmethod
    def resolve_teacher_username(obj):
        return obj.teacher.username

    @staticmethod
    def resolve_thumbnail(obj):
        return obj.thumbnail.url if obj.thumbnail else None


class CourseDetailSchema(CourseOutSchema):
    pass


class CourseListSchema(Schema):
    count: int
    page: int
    page_size: int
    results: list[CourseOutSchema]


class CourseFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=["title__icontains", "description__icontains"])
    teacher: Optional[int] = Field(None, q="teacher_id")
    price_gte: Optional[float] = Field(None, q="price__gte")
    price_lte: Optional[float] = Field(None, q="price__lte")

