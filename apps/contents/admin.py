from django.contrib import admin

from .models import CourseContent


@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "description", "course__title")
    autocomplete_fields = ("course",)
