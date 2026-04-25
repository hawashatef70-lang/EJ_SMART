from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # 🌐 WEB (لو لسه محتفظ بيه)
    # =========================
    path("", views.property_list, name="property_list"),
    path("create/", views.create_property, name="create_property"),
    path("<int:id>/", views.property_detail, name="property_detail"),


    # =========================
    # 🔥 API (REST STYLE)
    # =========================
    path("", views.api_properties, name="api_properties"),
    path("<int:id>/", views.api_property_detail, name="api_property_detail"),
    path("create/", views.api_create_property, name="api_create_property"),
    path("update/<int:id>/", views.api_update_property, name="api_update_property"),
    path("delete/<int:id>/", views.api_delete_property, name="api_delete_property"),
]