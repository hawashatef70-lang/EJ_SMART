from django.urls import path
from . import views

urlpatterns = [
    # =========================
    # WEB (OLD - KEEP AS IT IS)
    # =========================
    path("", views.property_list, name="property_list"),
    path("create/", views.create_property, name="create_property"),
    path("<int:id>/", views.property_detail, name="property_detail"),

    # =========================
    # API (NEW - SAFE ADDITION)
    # =========================
    path("api/properties/", views.api_properties, name="api_properties"),
    path("api/properties/<int:id>/", views.api_property_detail, name="api_property_detail"),
    path("api/properties/create/", views.api_create_property, name="api_create_property"),
    path("api/properties/update/<int:id>/", views.api_update_property),
    path("api/properties/delete/<int:id>/", views.api_delete_property),
    
]