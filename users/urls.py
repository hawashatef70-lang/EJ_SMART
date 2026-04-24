from django.urls import path
from .views import (
    api_register,
    api_login,
    api_logout,
    my_profile,
    update_profile
)

urlpatterns = [

    # 🟢 AUTH API
    path("register/", api_register, name="api-register"),
    path("login/", api_login, name="api-login"),
    path("logout/", api_logout, name="api-logout"),

    # 👤 USER PROFILE
    path("me/", my_profile, name="api-me"),
    path("update/", update_profile, name="api-update"),
]