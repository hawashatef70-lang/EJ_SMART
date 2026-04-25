from django.urls import path
from . import views

urlpatterns = [

    # 📩 كل الإشعارات
    path("", views.my_notifications),

    # ✔ إشعار واحد قرأ
    path("read/<int:notification_id>/", views.mark_as_read),

    # ✔ كلهم اتقرو
    path("read-all/", views.mark_all_as_read),

    # 🗑 حذف إشعار
    path("delete/<int:notification_id>/", views.delete_notification),

    # 🔢 عدد غير المقروء
    path("unread-count/", views.unread_count),
]