from django.urls import path
from .views import (
    api_create_contract,
    api_contract_detail,
    api_update_contract,
    api_delete_contract,
    api_sign_contract,
    api_send_contract,
    api_download_contract
)

urlpatterns = [

    # ➕ Create Contract
    path("create/", api_create_contract),

    # 📄 Detail
    path("<int:id>/", api_contract_detail),

    # ✏️ Update
    path("<int:id>/update/", api_update_contract),

    # 🗑 Delete
    path("<int:id>/delete/", api_delete_contract),

    # ✍️ Sign
    path("<int:id>/sign/", api_sign_contract),

    # 📤 Send
    path("<int:id>/send/", api_send_contract),

    # 📥 Download
    path("<int:id>/download/", api_download_contract),
]