from django.urls import path
from . import views
from .views import (
    api_contract_detail,
    api_sign_contract,
    api_download_contract,
    api_send_contract
)

urlpatterns = [

    # ======================
    # 🟦 WEB (OLD - متلمسوش)
    # ======================
    path("<int:id>/", views.contract_detail, name="contract_detail"),
    path("contract/<int:contract_id>/save-signature/", views.save_contract_signature, name="save_signature"),

    # ======================
    # 🟢 API (NEW)
    # ======================
    path("api/<int:id>/", api_contract_detail, name="api_contract_detail"),
    path("api/sign/<int:contract_id>/", api_sign_contract, name="api_sign_contract"),
    path("api/download/<int:id>/", api_download_contract, name="api_download_contract"),
    path("api/send/<int:id>/", api_send_contract, name="api_send_contract"),
]
