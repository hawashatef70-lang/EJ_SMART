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
    path("api/register/", api_register, name="api-register"),
    path("api/login/", api_login, name="api-login"),
    path("api/logout/", api_logout, name="api-logout"),

    # 👤 USER PROFILE
    path("api/me/", my_profile, name="api-me"),
    path("api/update/", update_profile, name="api-update"),
]