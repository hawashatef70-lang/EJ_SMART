from django.urls import path
from .views import (
    api_make_payment,
    my_payments,
    payment_detail,
)

urlpatterns = [

    # 💰 Create Payment
    path(
        "api/payments/<int:booking_id>/",
        api_make_payment,
        name="make_payment"
    ),

    # 📄 List My Payments
    path(
        "api/payments/",
        my_payments,
        name="my_payments"
    ),

    # 🔍 Payment Detail
    path(
        "api/payments/<int:payment_id>/detail/",
        payment_detail,
        name="payment_detail"
    ),
]