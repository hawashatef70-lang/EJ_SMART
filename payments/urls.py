from django.urls import path
from . import views

urlpatterns = [

    # ➕ Create Payment
    path("create/<int:booking_id>/", views.api_make_payment),

    # 📄 My Payments
    path("", views.my_payments),

    # 🔍 Detail
    path("<int:payment_id>/", views.payment_detail),

    # ✏️ Update
    path("<int:payment_id>/update/", views.update_payment),

    # 🗑 Delete
    path("<int:payment_id>/delete/", views.delete_payment),

]