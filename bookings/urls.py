from django.urls import path
from .views import create_booking, api_create_booking, my_bookings

urlpatterns = [

    # 🟦 WEB (OLD - KEEP)
    path('create/<int:property_id>/', create_booking, name='create_booking'),

    # 🟢 API (NEW)
    path("api/create/<int:property_id>/", api_create_booking),
    path("api/my/", my_bookings),
]