from django.urls import path
from .views import (
    api_contract_detail,
    api_sign_contract,
    api_download_contract,
    api_send_contract
)

urlpatterns = [

    path("api/contracts/<int:id>/", api_contract_detail, name="contract_detail"),

    path("api/contracts/<int:contract_id>/sign/", api_sign_contract, name="sign_contract"),

    path("api/contracts/<int:id>/send/", api_send_contract, name="send_contract"),

    path("api/contracts/<int:id>/download/", api_download_contract, name="download_contract"),
]
