import json
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Message

@csrf_exempt
@login_required
def send_message(request, user_id):
    """ إرسال رسالة من المستخدم الحالي إلى مستخدم آخر بخصوص عقار معين """
    if request.method == 'POST':
        # استقبال البيانات سواء كانت JSON أو Form Data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            text = data.get('message')
            prop_id = data.get('property_id')
        else:
            text = request.POST.get('message')
            prop_id = request.POST.get('property_id')

        if not text:
            return JsonResponse({"error": "المحتوى فارغ"}, status=400)

        msg = Message.objects.create(
            sender=request.user,
            receiver_id=user_id,
            message=text,
            property_id=prop_id
        )

        return JsonResponse({
            "status": "success",
            "message_id": msg.id,
            "created_at": msg.created_at.strftime("%I:%M %p")
        })
    return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def inbox(request):
    """ عرض قائمة الأشخاص الذين تواصل معهم المستخدم (مثل واجهة واتساب) """
    user = request.user
    # جلب كافة الرسائل الخاصة بالمستخدم
    all_msgs = Message.objects.filter(Q(sender=user) | Q(receiver=user))
    
    inbox_list = []
    seen_users = set()

    for m in all_msgs:
        other_user = m.receiver if m.sender == user else m.sender
        if other_user.id not in seen_users:
            seen_users.add(other_user.id)
            inbox_list.append({
                "user_id": other_user.id,
                "user_name": other_user.username,
                "last_message": m.message,
                "unread_count": Message.objects.filter(sender=other_user, receiver=user, is_read=False).count(),
                "time": m.created_at.strftime("%Y-%m-%d %H:%M")
            })
    
    return JsonResponse({"inbox": inbox_list}, safe=False)

@login_required
def chat_history(request, user_id):
    """ جلب تاريخ المحادثة مع مستخدم معين وتحديث الرسائل لـ 'مقروءة' """
    messages = Message.objects.filter(
        Q(sender=request.user, receiver_id=user_id) |
        Q(sender_id=user_id, receiver=request.user)
    ).order_by('created_at')

    # بمجرد فتح الشات، نعتبر الرسائل المستلمة "مقروءة"
    messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    data = [{
        "sender_id": m.sender.id,
        "sender_name": m.sender.username,
        "is_me": m.sender == request.user,
        "message": m.message,
        "property_id": m.property_id,
        "time": m.created_at.strftime("%I:%M %p"),
        "is_read": m.is_read
    } for m in messages]

    return JsonResponse({"chat": data}, safe=False)




from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .models import Message
from .serializers import MessageSerializer


# =========================
# 💬 SEND MESSAGE
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_send_message(request, user_id):

    text = request.data.get("message")
    prop_id = request.data.get("property_id")

    if not text:
        return Response({"error": "Message is empty"}, status=400)

    msg = Message.objects.create(
        sender=request.user,
        receiver_id=user_id,
        message=text,
        property_id=prop_id
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
    ).order_by('created_at')

    messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    return Response(MessageSerializer(messages, many=True).data)


# =========================
# 📥 INBOX (Chat List)
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
        other = m.receiver if m.sender == user else m.sender

        if other.id not in seen:
            seen.add(other.id)

            inbox.append({
                "user_id": other.id,
                "username": other.username,
                "last_message": m.message,
                "property_id": m.property_id,
                "time": m.created_at,
                "unread_count": Message.objects.filter(
                    sender=other,
                    receiver=user,
                    is_read=False
                ).count()
            })

    return Response(inbox)

# Create your views here.
