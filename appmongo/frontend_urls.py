from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="core"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", views.dashboard_page, name="dashboard"),
    path("courses/", views.course_list, name="course_list"),
    path("courses/create/", views.create_course, name="create_course"),
    path("courses/<int:course_id>/", views.course_detail, name="course_detail"),
    path("courses/<int:course_id>/edit/", views.edit_course, name="edit_course"),
    path("courses/<int:course_id>/delete/", views.delete_course, name="delete_course"),
    path("courses/<int:course_id>/join/", views.join_course, name="join_course"),
    path(
        "courses/<int:course_id>/contents/",
        views.course_content_list,
        name="course_content_list",
    ),
    path(
        "courses/<int:course_id>/contents/add/",
        views.add_content,
        name="add_content",
    ),
    path(
        "contents/<int:content_id>/",
        views.course_content_detail,
        name="course_content_detail",
    ),
    path("contents/<int:content_id>/comment/", views.add_comment, name="add_comment"),
    path(
        "contents/<int:content_id>/edit/",
        views.edit_content,
        name="edit_content",
    ),
    path(
        "contents/<int:content_id>/delete/",
        views.delete_content,
        name="delete_content",
    ),
    path("my-courses/", views.my_courses, name="my_courses"),
    path("import-csv/", views.import_csv, name="import_csv"),
    path("download-csv-template/", views.download_csv_template, name="download_csv_template"),
]
