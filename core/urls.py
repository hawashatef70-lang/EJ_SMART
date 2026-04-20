from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),  # 👈 endpoint الرئيسي
    path("dashboard/", views.dashboard),
    path("search/", views.search),
]