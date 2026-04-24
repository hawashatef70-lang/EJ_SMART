from django.urls import path
from .views import create_booking, api_create_booking, my_bookings

urlpatterns = [

    # ======================
    # 🟦 WEB (OLD - optional keep)
    # ======================
    path('create/<int:property_id>/', create_booking, name='create_booking'),

    # ======================
    # 🟢 API (CLEAN VERSION)
    # ======================
    path('create/<int:property_id>/', api_create_booking, name='api_create_booking'),
    path('my/', my_bookings, name='my_bookings'),
]