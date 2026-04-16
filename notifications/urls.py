from django.urls import path
from .views import (
    list_notifications,
    mark_as_read,
    api_notifications,
    api_mark_as_read
)

urlpatterns = [

    # 🟦 WEB (OLD - KEEP)
    path('', list_notifications, name='notifications'),
    path('read/<int:notification_id>/', mark_as_read, name='mark_read'),

    # 🟢 API (NEW)
    path("api/", api_notifications),
    path("api/read/<int:notification_id>/", api_mark_as_read),

]