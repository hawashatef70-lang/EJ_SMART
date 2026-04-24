from django.contrib import admin
from django.utils.html import format_html

from .models import Contract, ContractSignature


# =========================
# ✍️ SIGNATURE INLINE
# =========================
class SignatureInline(admin.StackedInline):

    model = ContractSignature
    extra = 0

    fields = ('signature_image', 'signature_preview')
    readonly_fields = ('signature_preview',)

    verbose_name = "Contract Signature"
    verbose_name_plural = "Contract Signature"

    def signature_preview(self, obj):
        if obj.signature_image:
            return format_html(
                '<img src="{}" width="220" style="border:1px solid #ddd; padding:5px; border-radius:8px; background:#fff;" />',
                obj.signature_image.url
            )
        return "No signature uploaded"

    signature_preview.short_description = "Preview"


# =========================
# 📄 CONTRACT ADMIN
# =========================
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):

    # 🟢 Table view
    list_display = (
        'id',
        'booking',
        'signed',
        'created_at'
    )

    # 🟢 Filters
    list_filter = (
        'signed',
        'created_at'
    )

    # 🟢 Search
    search_fields = (
        'booking__id',
        'booking__property__title',
        'booking__tenant__username'
    )

    # 🟢 Performance
    list_select_related = ('booking',)

    # 🟢 Ordering
    ordering = ('-created_at',)

    # 🟢 Inline signature
    inlines = [SignatureInline]

    # 🟢 Read-only protection (important)
    readonly_fields = ('created_at',)
# Register your models here.
