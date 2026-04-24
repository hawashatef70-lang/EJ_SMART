from django.contrib import admin
from .models import Property, PropertyImage, PropertyVideo


# =========================
# 🖼️ Property Images Inline
# =========================
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ["image"]


# =========================
# 🎥 Property Videos Inline
# =========================
class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 1
    fields = ["video"]


# =========================
# 🏠 Property Admin
# =========================
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "owner",
        "property_type",
        "city",
        "price",
        "area",
        "is_available",
        "created_at",
    )

    list_filter = (
        "property_type",
        "city",
        "is_available",
        "bedrooms",
        "bathrooms",
        "price",
        "area",
    )

    search_fields = (
        "title",
        "city",
        "address",
        "owner__username",
    )

    list_editable = (
        "price",
        "is_available",
        "property_type",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("owner", "title", "description", "property_type")
        }),
        ("Location", {
            "fields": ("city", "address")
        }),
        ("Details", {
            "fields": ("price", "area", "bedrooms", "bathrooms", "is_available")
        }),
    )

    inlines = [PropertyImageInline, PropertyVideoInline]


# =========================
# 📦 Optional registrations
# =========================
admin.site.register(PropertyImage)
admin.site.register(PropertyVideo)