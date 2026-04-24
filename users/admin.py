from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "username",
        "email",
        "user_type",
        "phone",
        "is_verified",
        "created_at",
    )

    list_filter = (
        "user_type",
        "is_verified",
        "created_at",
    )

    search_fields = (
        "username",
        "email",
        "phone",
    )

    list_editable = (
        "user_type",
        "is_verified",
        "phone",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)