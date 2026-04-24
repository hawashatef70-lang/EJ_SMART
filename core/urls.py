from django.urls import path
from . import views

urlpatterns = [

    # ======================
    # 🏠 MAIN PAGES
    # ======================
    path("", views.home, name="home"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("search/", views.search, name="search"),
]