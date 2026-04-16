from django.contrib import admin
from .models import Handover

@admin.register(Handover)
class HandoverAdmin(admin.ModelAdmin):

    list_display = (
        'property',
        'tenant',
        'owner',
        'status',
        'is_confirmed_by_owner',
        'is_confirmed_by_tenant',
        'created_at'
    )

    list_filter = ('status',)

    search_fields = ('property__title', 'tenant__username', 'owner__username')

# Register your models here.
