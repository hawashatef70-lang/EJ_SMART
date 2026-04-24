from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    # ======================
    # 📊 LIST DISPLAY
    # ======================
    list_display = (
        "user",
        "property",
        "rating",
        "created_at"
    )

    # ======================
    # 🔎 SEARCH
    # ======================
    search_fields = (
        "user__username",
        "property__title",
        "review_text",
    )

    # ======================
    # 📌 FILTERS
    # ======================
    list_filter = (
        "rating",
        "created_at",
    )

    # ======================
    # ⚡ ORDERING
    # ======================
    ordering = ("-created_at",)
# Register your models here.
