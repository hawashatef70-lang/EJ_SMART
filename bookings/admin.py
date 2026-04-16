from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'tenant', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date')
    
    # جربنا title و name ومنفعوش، يبقى الحقل عندك غالباً address 
    # أنا ضفت لك كل الاحتمالات الممكنة عشان "المعمورة" تظهر وما يطلعش Error
    search_fields = (
        'property__address', 
        'property__title', 
        'tenant__username',
        'status'
    )