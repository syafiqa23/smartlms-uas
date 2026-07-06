from ninja import Schema


class ChartPointSchema(Schema):
    label: str
    value: int


class RecentActivitySchema(Schema):
    type: str
    label: str
    created_at: str


class DashboardSchema(Schema):
    total_course: int
    total_student: int
    total_teacher: int
    total_comment: int
    total_content: int
    course_chart: list[ChartPointSchema]
    user_chart: list[ChartPointSchema]
    enrollment_chart: list[ChartPointSchema]
    recent_activity: list[RecentActivitySchema]
