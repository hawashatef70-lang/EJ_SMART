from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import Handover
from bookings.models import Booking
from .serializers import HandoverSerializer


# =========================
# 🟢 CREATE
# =========================
@extend_schema(tags=["Handover"])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_handover(request):

    booking_id = request.data.get("booking_id")

    if not booking_id:
        return Response({"error": "booking_id is required"}, status=400)

    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.tenant and request.user != booking.property.owner:
        return Response({"error": "Not allowed"}, status=403)

    if Handover.objects.filter(booking=booking).exists():
        return Response({"error": "Already exists"}, status=400)

    handover = Handover.objects.create(
        property=booking.property,
        tenant=booking.tenant,
        owner=booking.property.owner,
        booking=booking
    )

    return Response({
        "status": "success",
        "message": "Handover created",
        "data": HandoverSerializer(handover).data
    })


# =========================
# 🟢 CONFIRM
# =========================
@extend_schema(tags=["Handover"])
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def confirm_handover(request):

    handover_id = request.data.get("handover_id")

    if not handover_id:
        return Response({"error": "handover_id is required"}, status=400)

    handover = get_object_or_404(Handover, id=handover_id)

    if request.user not in [handover.owner, handover.tenant]:
        return Response({"error": "Not allowed"}, status=403)

    if request.user == handover.owner:
        handover.is_confirmed_by_owner = True

    if request.user == handover.tenant:
        handover.is_confirmed_by_tenant = True

    if handover.is_confirmed_by_owner and handover.is_confirmed_by_tenant:
        handover.status = "completed"

    handover.save()

    return Response({
        "status": "success",
        "message": "Handover confirmed",
        "data": HandoverSerializer(handover).data
    })


# =========================
# 🟢 DELETE
# =========================
@extend_schema(tags=["Handover"])
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_handover(request):

    handover_id = request.data.get("handover_id")

    if not handover_id:
        return Response({"error": "handover_id is required"}, status=400)

    handover = get_object_or_404(Handover, id=handover_id)

    if request.user != handover.owner:
        return Response({"error": "Only owner can delete"}, status=403)

    handover.delete()

    return Response({
        "status": "success",
        "message": "Deleted successfully"
    })


# =========================
# 🟢 MY HANDOVERS
# =========================
@extend_schema(tags=["Handover"])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_handovers(request):

    handovers = Handover.objects.filter(
        Q(owner=request.user) | Q(tenant=request.user)
    )

    return Response({
        "status": "success",
        "data": HandoverSerializer(handovers, many=True).data
    })


# =========================
# 🟢 DETAIL
# =========================
@extend_schema(tags=["Handover"])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def handover_detail(request, id):

    handover = get_object_or_404(Handover, id=id)

    if request.user not in [handover.owner, handover.tenant]:
        return Response({"error": "Not allowed"}, status=403)

    return Response({
        "status": "success",
        "data": HandoverSerializer(handover).data
    })
# Create your views here.
