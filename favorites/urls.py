from django.urls import path
from .views import (
    toggle_favorite,
    list_favorites,
    favorite_detail,
    clear_favorites
)

urlpatterns = [

    # ======================
    # 🟢 FAVORITES API ONLY
    # ======================

    # 📄 Get all favorites
    path(
        "favorites/",
        list_favorites,
        name="list_favorites"
    ),

    # 🔥 Toggle favorite (add/remove in one endpoint)
    path(
        "favorites/toggle/<int:property_id>/",
        toggle_favorite,
        name="toggle_favorite"
    ),

    # 🔍 Single favorite detail
    path(
        "favorites/<int:favorite_id>/",
        favorite_detail,
        name="favorite_detail"
    ),

    # 🗑 Clear all favorites
    path(
        "favorites/clear/",
        clear_favorites,
        name="clear_favorites"
    ),
]