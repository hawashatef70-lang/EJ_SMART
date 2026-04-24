from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message
from .serializers import MessageSerializer


# =========================
# 💬 SEND MESSAGE
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_send_message(request, user_id):

    text = request.data.get("message")
    property_id = request.data.get("property")

    if not text:
        return Response({"error": "Message is empty"}, status=400)

    msg = Message.objects.create(
        sender=request.user,
        receiver_id=user_id,
        message=text,
        property_id=property_id
    )

    return Response(MessageSerializer(msg).data)


# =========================
# 💬 CHAT HISTORY
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_chat_history(request, user_id):

    messages = Message.objects.filter(
        Q(sender=request.user, receiver_id=user_id) |
        Q(sender_id=user_id, receiver=request.user)
    ).select_related('sender', 'receiver').order_by('created_at')

    # mark messages as read
    Message.objects.filter(
        sender_id=user_id,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    return Response(MessageSerializer(messages, many=True).data)


# =========================
# 📥 INBOX
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_inbox(request):

    user = request.user

    messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-created_at')

    seen = set()
    inbox = []

    for m in messages:
        other_user = m.receiver if m.sender == user else m.sender

        if other_user.id not in seen:
            seen.add(other_user.id)

            unread_count = Message.objects.filter(
                sender=other_user,
                receiver=user,
                is_read=False
            ).count()

            inbox.append({
                "user_id": other_user.id,
                "username": other_user.username,
                "last_message": m.message,
                "property_id": m.property_id,
                "time": m.created_at,
                "unread_count": unread_count
            })

    return Response(inbox)

# Create your views here.
