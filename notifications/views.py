from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


# =========================
# 📩 GET MY NOTIFICATIONS
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    serializer = NotificationSerializer(notifications, many=True)

    return Response(serializer.data)


# =========================
# ✔ MARK AS READ
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    notification.is_read = True
    notification.save()

    return Response({"message": "Marked as read"})


# =========================
# ✔ MARK ALL AS READ 🔥
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):

    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)

    return Response({"message": "All notifications marked as read"})


# =========================
# 🗑 DELETE NOTIFICATION
# =========================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    notification.delete()

    return Response({"message": "Deleted successfully"})


# =========================
# 🔢 UNREAD COUNT (IMPORTANT)
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count(request):

    count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return Response({"unread_count": count})
# Create your views here.
