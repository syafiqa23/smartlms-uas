from datetime import datetime

from ninja import Schema


class CourseMemberSchema(Schema):
    id: int
    course_id: int
    user_id: int
    username: str
    role: str
    joined_at: datetime

    @staticmethod
    def resolve_username(obj):
        return obj.user.username


class EnrollmentSchema(Schema):
    id: int
    course_id: int
    student_id: int
    student_username: str
    is_active: bool
    enrolled_at: datetime

    @staticmethod
    def resolve_student_username(obj):
        return obj.student.username
