from django.urls import path
from .views import add_review, property_reviews

urlpatterns = [

    # ======================
    # 🟢 REVIEWS API
    # ======================

    path("add/<int:property_id>/", add_review, name="add_review"),

    path("property/<int:property_id>/", property_reviews, name="property_reviews"),
]