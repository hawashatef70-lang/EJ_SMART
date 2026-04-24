from django.urls import path
from .views import (
    create_handover,
    confirm_handover,
    my_handovers,
    handover_detail,
    delete_handover
)

urlpatterns = [

    # ======================
    # 🟢 HANDOVER API
    # ======================

    # ➕ Create handover
    path(
        "api/handovers/create/<int:booking_id>/",
        create_handover,
        name="create_handover"
    ),

    # ✔ Confirm handover (owner/tenant)
    path(
        "api/handovers/confirm/<int:handover_id>/",
        confirm_handover,
        name="confirm_handover"
    ),

    # 📄 My handovers
    path(
        "api/handovers/my/",
        my_handovers,
        name="my_handovers"
    ),

    # 🔍 Single handover detail
    path(
        "api/handovers/<int:handover_id>/",
        handover_detail,
        name="handover_detail"
    ),

    # 🗑 Delete handover (optional admin/owner control)
    path(
        "api/handovers/delete/<int:handover_id>/",
        delete_handover,
        name="delete_handover"
    ),
]