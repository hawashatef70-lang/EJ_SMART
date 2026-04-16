from django.urls import path
from .views import (
    send_message,
    inbox,
    chat_history,
    api_send_message,
    api_chat_history,
    api_inbox
)

urlpatterns = [

    # 🟦 WEB (OLD - KEEP)
    path('send/<int:user_id>/', send_message, name='send_message'),
    path('inbox/', inbox, name='inbox'),
    path('history/<int:user_id>/', chat_history, name='chat_history'),

    # 🟢 API (NEW)
    path("api/send/<int:user_id>/", api_send_message),
    path("api/history/<int:user_id>/", api_chat_history),
    path("api/inbox/", api_inbox),
]