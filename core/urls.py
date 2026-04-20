from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),  # 👈 الجديد
    path("dashboard/", views.dashboard),
    path("search/", views.search),
]