from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def list_notifications(request):

    notes = Notification.objects.filter(user=request.user).order_by('-created_at')

    data = [
        {
            "id": n.id,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in notes
    ]

    return JsonResponse(data, safe=False)


@login_required
def mark_as_read(request, notification_id):

    note = get_object_or_404(Notification, id=notification_id, user=request.user)
    note.is_read = True
    note.save()

    return JsonResponse({"message": "Marked"})


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Notification
from .serializers import NotificationSerializer


# =========================
# 📩 GET NOTIFICATIONS
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_notifications(request):

    notes = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    serializer = NotificationSerializer(notes, many=True)

    return Response(serializer.data)


# =========================
# ✔ MARK AS READ
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_mark_as_read(request, notification_id):

    note = get_object_or_404(Notification, id=notification_id, user=request.user)
    note.is_read = True
    note.save()

    return Response({"message": "Marked as read"})
# Create your views here.
