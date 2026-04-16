from django.urls import path
from .views import (
    register, login_view, logout_view, dashboard,
    api_register, api_login,
    my_profile, update_profile
)

urlpatterns = [

    # 🟦 WEB (لو عندك صفحات قديمة)
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),

    # 🟢 API (اللي هنشتغل عليه في Postman)
    path("api/register/", api_register),
    path("api/login/", api_login),
    path("api/me/", my_profile),
    path("api/update/", update_profile),
]