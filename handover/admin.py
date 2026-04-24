from django.contrib import admin
from .models import Handover


@admin.register(Handover)
class HandoverAdmin(admin.ModelAdmin):

    # =========================
    # 🟢 TABLE VIEW
    # =========================
    list_display = (
        'id',
        'property',
        'tenant',
        'owner',
        'status',
        'is_confirmed_by_owner',
        'is_confirmed_by_tenant',
        'created_at'
    )

    # =========================
    # 🟢 FILTERS
    # =========================
    list_filter = (
        'status',
        'is_confirmed_by_owner',
        'is_confirmed_by_tenant',
        'created_at'
    )

    # =========================
    # 🟢 SEARCH
    # =========================
    search_fields = (
        'property__title',
        'tenant__username',
        'owner__username'
    )

    # =========================
    # 🟢 QUICK EDIT
    # =========================
    list_editable = (
        'status',
        'is_confirmed_by_owner',
        'is_confirmed_by_tenant'
    )

    # =========================
    # 🟢 ORDERING
    # =========================
    ordering = ('-created_at',)

    # =========================
    # 🟢 PERFORMANCE
    # =========================
    list_select_related = (
        'property',
        'tenant',
        'owner'
    )

    # =========================
    # 🟢 PAGINATION
    # =========================
    list_per_page = 25

    # =========================
    # 🟢 DATE NAVIGATION
    # =========================
    date_hierarchy = 'created_at'

    # =========================
    # 🟢 BULK ACTIONS 🔥
    # =========================
    actions = [
        'mark_completed',
        'mark_pending'
    ]

    def mark_completed(self, request, queryset):
        queryset.update(status='completed')

    mark_completed.short_description = "Mark selected as Completed"

    def mark_pending(self, request, queryset):
        queryset.update(status='pending')

    mark_pending.short_description = "Mark selected as Pending"

# Register your models here.
