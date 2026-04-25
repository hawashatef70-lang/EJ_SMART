from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_handover),
    path("confirm/", views.confirm_handover),
    path("delete/", views.delete_handover),
    path("my/", views.my_handovers),
    path("<int:id>/", views.handover_detail),
]