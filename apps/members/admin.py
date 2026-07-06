from django.contrib import admin

from .models import CourseMember, Enrollment


@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "role", "joined_at")
    list_filter = ("role", "joined_at")
    search_fields = ("user__username", "course__title")
    autocomplete_fields = ("course", "user")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "is_active", "enrolled_at")
    list_filter = ("is_active", "enrolled_at")
    search_fields = ("student__username", "course__title")
    autocomplete_fields = ("course", "student")
