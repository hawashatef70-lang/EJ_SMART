from django.urls import path
from . import views

urlpatterns = [

    # 🟢 LIST + CREATE
    path("", views.api_properties, name="api_properties"),

    # 🟢 DETAIL + UPDATE + DELETE
    path("<int:id>/", views.api_property_detail, name="api_property_detail"),

]