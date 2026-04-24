from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    # =========================
    # 📊 TABLE DISPLAY
    # =========================
    list_display = (
        'id',
        'sender',
        'receiver',
        'property_id',
        'short_message',
        'is_read',
        'created_at'
    )

    # =========================
    # 🔍 FILTERS
    # =========================
    list_filter = (
        'is_read',
        'created_at',
        'sender',
        'receiver'
    )

    # =========================
    # 🔎 SEARCH
    # =========================
    search_fields = (
        'message',
        'sender__username',
        'receiver__username',
    )

    # =========================
    # ⚡ PERFORMANCE
    # =========================
    list_select_related = ('sender', 'receiver')

    # =========================
    # 📦 READ ONLY
    # =========================
    readonly_fields = (
        'created_at',
    )

    # =========================
    # 📄 ORDERING
    # =========================
    ordering = ('-created_at',)

    # =========================
    # ✨ CUSTOM DISPLAY
    # =========================
    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    short_message.short_description = "Message Preview"
# Register your models here.
