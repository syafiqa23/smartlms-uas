from typing import Any

from ninja import Schema


class MessageSchema(Schema):
    message: str


class ErrorSchema(Schema):
    detail: str


class PaginatedSchema(Schema):
    count: int
    page: int
    page_size: int
    results: list[Any]
