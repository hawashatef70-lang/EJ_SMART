from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "booking",
        "amount",
        "payment_method",
        "status",
        "created_at"
    )

    list_filter = (
        "payment_method",
        "status",
        "created_at"
    )

    search_fields = (
        "booking__id",
        "booking__user__username"
    )

    ordering = ("-created_at",)
# Register your models here.
