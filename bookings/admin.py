from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    # ======================
    # 📊 LIST DISPLAY
    # ======================
    list_display = (
        'id',
        'property',
        'tenant',
        'start_date',
        'end_date',
        'status'
    )

    # ======================
    # 🔎 FILTERS
    # ======================
    list_filter = (
        'status',
        'start_date',
        'end_date'
    )

    # ======================
    # 🔍 SEARCH (CLEAN + RELIABLE)
    # ======================
    search_fields = (
        'property__title',
        'property__address',
        'tenant__username',
        'tenant__email',
    )

    # ======================
    # ⚡ QUICK EDIT (OPTIONAL)
    # ======================
    list_editable = (
        'status',
    )

    # ======================
    # 📅 ORDERING
    # ======================
    ordering = ('-id',)