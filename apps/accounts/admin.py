from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as AuthUser

from .models import User

# Unregister the default auth.User from admin
try:
    admin.site.unregister(AuthUser)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class SmartLMSUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Smart LMS Profile", {"fields": ("role", "avatar", "bio")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Smart LMS Profile", {"fields": ("role", "avatar", "bio")}),
    )
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
