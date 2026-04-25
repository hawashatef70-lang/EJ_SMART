from django.urls import path
from .views import (
    api_create_booking,
    my_bookings,
    booking_detail,
    update_booking,
    delete_booking
)

urlpatterns = [

    # ➕ Create booking
    path("create/<int:property_id>/", api_create_booking),

    # 📄 My bookings
    path("my/", my_bookings),

    # 🔍 Detail booking
    path("<int:id>/", booking_detail),

    # ✏️ Update booking
    path("<int:id>/update/", update_booking),

    # 🗑 Delete booking
    path("<int:id>/delete/", delete_booking),
]