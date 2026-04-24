from django.contrib import admin
from .models import SiteSettings, AuditLog


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "maintenance_mode", "updated_at")
    list_editable = ("maintenance_mode",)
    search_fields = ("site_name",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "model_name", "created_at")
    list_filter = ("action", "model_name", "created_at")
    search_fields = ("user__username", "action", "model_name")
    readonly_fields = ("user", "action", "model_name", "created_at")
    ordering = ("-created_at",)
# Register your models here.
