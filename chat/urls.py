from django.urls import path
from .views import (
    api_send_message,
    api_inbox,
    api_chat_history
)

urlpatterns = [

    # 📩 send message
    path("api/messages/send/<int:user_id>/", api_send_message),

    # 📥 inbox
    path("api/messages/inbox/", api_inbox),

    # 💬 chat history
    path("api/messages/conversation/<int:user_id>/", api_chat_history),
]