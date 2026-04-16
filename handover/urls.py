from django.urls import path
from .views import create_handover, confirm_handover, my_handovers

urlpatterns = [

    # ======================
    # 🟦 HANDOVER API
    # ======================

    # إنشاء handover
    path("create/<int:booking_id>/", create_handover, name="create_handover"),

    # تأكيد handover (مالك / مستأجر)
    path("confirm/<int:handover_id>/", confirm_handover, name="confirm_handover"),

    # عرض handovers الخاصة بالمستخدم
    path("my/", my_handovers, name="my_handovers"),
]