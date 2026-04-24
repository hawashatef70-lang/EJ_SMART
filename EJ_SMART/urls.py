"""
URL configuration for EJ_SMART project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# 👇 Home API
def home(request):
    return JsonResponse({
        "project": "EJ SMART API",
        "status": "running 🚀",
        "base_url": "https://ejsmart-production.up.railway.app",

        "documentation": {
            "swagger": "/api/docs/",
            "schema": "/api/schema/"
        },

        "auth": {
            "login": "/api/token/",
            "refresh": "/api/token/refresh/",
        },

        "endpoints": {
            "admin": "/admin/",
            "users": "/api/users/",
            "properties": "/api/properties/",
            "bookings": "/api/bookings/",
            "contracts": "/api/contracts/",
            "payments": "/api/payments/",
            "reviews": "/api/reviews/",
            "chat": "/api/chat/",
            "handover": "/api/handover/",
            "favorites": "/api/favorites/",
            "notifications": "/api/notifications/",
        }
    })



urlpatterns = [
    path("admin/", admin.site.urls),

    # 🔐 JWT
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # 📦 APIs
    path('api/', include('users.urls')),
    path("properties/", include("properties.urls")),
    path("bookings/", include("bookings.urls")),
    path("contracts/", include("contracts.urls")),
    path("payments/", include("payments.urls")),
    path("reviews/", include("reviews.urls")),
    path("chat/", include("chat.urls")),
    path("handover/", include("handover.urls")),
    path("favorites/", include("favorites.urls")),
    path("notifications/", include("notifications.urls")),

    # 📄 Schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),


    # 📘 Swagger نسخة تانية
  path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)