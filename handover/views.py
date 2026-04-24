from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Handover
from bookings.models import Booking
from .serializers import HandoverSerializer


# =========================
# 🟢 CREATE HANDOVER
# =========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_handover(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    # 🔐 permission check
    if request.user != booking.tenant and request.user != booking.property.owner:
        return Response({"error": "Not allowed"}, status=403)

    # 🚫 prevent duplicates
    if Handover.objects.filter(booking=booking).exists():
        return Response({"error": "Already exists"}, status=400)

    handover = Handover.objects.create(
        property=booking.property,
        tenant=booking.tenant,
        owner=booking.property.owner,
        booking=booking
    )

    serializer = HandoverSerializer(handover)

    return Response({
        "message": "Handover created",
        "data": serializer.data
    })


# =========================
# 🟢 CONFIRM HANDOVER
# =========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_handover(request, handover_id):

    handover = get_object_or_404(Handover, id=handover_id)

    # 🔐 only owner or tenant
    if request.user not in [handover.owner, handover.tenant]:
        return Response({"error": "Not allowed"}, status=403)

    if request.user == handover.owner:
        handover.is_confirmed_by_owner = True

    if request.user == handover.tenant:
        handover.is_confirmed_by_tenant = True

    # 🔥 auto complete
    if handover.is_confirmed_by_owner and handover.is_confirmed_by_tenant:
        handover.status = "completed"

    handover.save()

    serializer = HandoverSerializer(handover)

    return Response({
        "message": "Handover updated",
        "data": serializer.data
    })


# =========================
# 🟢 MY HANDOVERS
# =========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_handovers(request):

    handovers = Handover.objects.filter(
        Q(owner=request.user) | Q(tenant=request.user)
    )

    serializer = HandoverSerializer(handovers, many=True)

    return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def handover_detail(request, handover_id):

    handover = get_object_or_404(Handover, id=handover_id)

    if request.user not in [handover.owner, handover.tenant]:
        return Response({"error": "Not allowed"}, status=403)

    serializer = HandoverSerializer(handover)
    return Response(serializer.data)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_handover(request, handover_id):

    handover = get_object_or_404(Handover, id=handover_id)

    if request.user != handover.owner:
        return Response({"error": "Only owner can delete"}, status=403)

    handover.delete()

    return Response({"message": "Deleted successfully"})
# Create your views here.
