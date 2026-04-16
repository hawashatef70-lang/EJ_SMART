from django.urls import path
from .views import (
    add_favorite,
    remove_favorite,
    list_favorites,
    api_add_favorite,
    api_remove_favorite,
    api_list_favorites
)

urlpatterns = [

    # ======================
    # 🟦 WEB (OLD - KEEP)
    # ======================

    path("add/<int:property_id>/", add_favorite, name="add_favorite"),
    path("remove/<int:property_id>/", remove_favorite, name="remove_favorite"),
    path("", list_favorites, name="list_favorites"),

    # ======================
    # 🟢 API (NEW)
    # ======================

    path("api/add/<int:property_id>/", api_add_favorite, name="api_add_favorite"),
    path("api/remove/<int:property_id>/", api_remove_favorite, name="api_remove_favorite"),
    path("api/", api_list_favorites, name="api_list_favorites"),
]
