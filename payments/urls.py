from django.urls import path
from .views import *

urlpatterns = [

    path("pay/<int:booking_id>/", make_payment, name="make_payment"),

    path("list/", payment_list, name="payment_list"),

]

urlpatterns = [

    # API
    path("api/pay/<int:booking_id>/", api_make_payment),
    path("api/my/", my_payments),

    # القديم
    path("pay/<int:booking_id>/", make_payment),
]