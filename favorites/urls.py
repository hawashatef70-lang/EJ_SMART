from django.urls import path
from . import views

urlpatterns = [

    # ❤️ كل المفضلة
    path("", views.list_favorites),

    # 🔥 إضافة / حذف (toggle)
    path("toggle/<int:property_id>/", views.toggle_favorite),

    # 🔍 تفاصيل مفضلة واحدة
    path("<int:favorite_id>/", views.favorite_detail),

    # 🗑 حذف كل المفضلة
    path("clear/", views.clear_favorites),
]