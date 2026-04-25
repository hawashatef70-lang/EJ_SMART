from django.urls import path
from .views import (
    api_send_message,
    api_inbox,
    api_chat_history,
    mark_as_read
)

urlpatterns = [

    # 💬 send message
    path("send/<int:user_id>/", api_send_message),

    # 📥 inbox
    path("inbox/", api_inbox),

    # 💬 chat
    path("chat/<int:user_id>/", api_chat_history),

    # ✔ mark message as read (optional but useful)
    path("read/<int:user_id>/", mark_as_read),

]
