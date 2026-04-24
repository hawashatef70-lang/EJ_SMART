from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    # =========================
    # 🟢 TABLE VIEW
    # =========================
    list_display = (
        "id",
        "user",
        "short_message",
        "is_read",
        "created_at"
    )

    list_filter = (
        "is_read",
        "created_at"
    )

    search_fields = (
        "user__username",
        "message"
    )

    list_editable = (
        "is_read",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_per_page = 25

    # =========================
    # 🟢 PERFORMANCE
    # =========================
    list_select_related = ("user",)

    # =========================
    # 🟢 CUSTOM DISPLAY
    # =========================
    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    short_message.short_description = "Message"

    # =========================
    # 🟢 BULK ACTIONS (IMPORTANT)
    # =========================
    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    mark_as_read.short_description = "Mark selected as Read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

    mark_as_unread.short_description = "Mark selected as Unread"

# Register your models here.
