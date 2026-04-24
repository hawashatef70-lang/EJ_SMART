from django.urls import path
from .views import (
    api_send_message,
    api_inbox,
    api_chat_history
)

urlpatterns = [

    # 📩 send message
    path("messages/send/<int:user_id>/", api_send_message),

    # 📥 inbox
    path("messages/inbox/", api_inbox),

    # 💬 chat history
    path("messages/conversation/<int:user_id>/", api_chat_history),
]