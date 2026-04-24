from django.urls import path
from .views import (
    my_notifications,
    mark_as_read,
    delete_notification
)

urlpatterns = [

    # =========================
    # 🟢 API ONLY (CLEAN)
    # =========================
    path("notifications/", my_notifications, name="my_notifications"),
    
    path(
        "notifications/read/<int:notification_id>/",
        mark_as_read,
        name="mark_notification_read"
    ),

    path(
        "notifications/delete/<int:notification_id>/",
        delete_notification,
        name="delete_notification"
    ),
]