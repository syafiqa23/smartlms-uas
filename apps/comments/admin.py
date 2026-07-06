from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "content", "parent", "created_at")
    list_filter = ("created_at",)
    search_fields = ("text", "user__username", "course__title", "content__title")
    autocomplete_fields = ("course", "content", "user", "parent")
