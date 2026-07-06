from ninja import NinjaAPI
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth

from apps.accounts.api.router import router as accounts_router
from apps.accounts.api.users_router import router as users_router
from apps.comments.api.router import router as comments_router
from apps.contents.api.router import router as contents_router
from apps.courses.api.router import router as courses_router
from apps.dashboard.api.router import router as dashboard_router
from apps.dashboard.api.statistics_router import router as statistics_router
from apps.members.api.router import router as members_router


# Inisialisasi API dengan HttpJwtAuth sesuai Django Ninja documentation
apiAuth = HttpJwtAuth()

api = NinjaAPI(
    title="Smart LMS",
    version="1.0.0",
    description="Smart Learning Management System API untuk UAS Pemrograman Sisi Server",
    urls_namespace="smart_lms_api",
    auth=apiAuth,
)

# Add routers untuk menstruktur endpoint berdasarkan resource
api.add_router("/auth/", accounts_router)
api.add_router("/users/", users_router)
api.add_router("/courses/", courses_router)
api.add_router("/course-members/", members_router)
api.add_router("/course-contents/", contents_router)
api.add_router("/comments/", comments_router)
api.add_router("/dashboard/", dashboard_router)
api.add_router("/statistics/", statistics_router)
