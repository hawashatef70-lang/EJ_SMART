from django.contrib import admin
from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):

    # =========================
    # 🟢 TABLE VIEW
    # =========================
    list_display = (
        'id',
        'user',
        'property',
        'created_at'
    )

    # =========================
    # 🟢 FILTERS
    # =========================
    list_filter = (
        'created_at',
        'user',
    )

    # =========================
    # 🟢 SEARCH
    # =========================
    search_fields = (
        'user__username',
        'property__title'
    )

    # =========================
    # 🟢 ORDERING
    # =========================
    ordering = ('-created_at',)

    # =========================
    # 🟢 PERFORMANCE
    # =========================
    list_select_related = ('user', 'property')

    # =========================
    # 🟢 PAGINATION
    # =========================
    list_per_page = 25

# Register your models here.
