from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer
from properties.models import Property


# =========================
# ➕ CREATE BOOKING
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_booking(request, property_id):

    property_obj = get_object_or_404(Property, id=property_id)

    serializer = BookingSerializer(data=request.data)

    if serializer.is_valid():

        with transaction.atomic():
            booking = serializer.save(
                tenant=request.user,
                property=property_obj
            )

        return Response(BookingSerializer(booking).data)

    return Response(serializer.errors, status=400)


# =========================
# 📄 MY BOOKINGS
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bookings(request):

    bookings = Booking.objects.filter(
        tenant=request.user
    ).select_related('property')

    serializer = BookingSerializer(bookings, many=True)

    return Response(serializer.data)


# =========================
# 🔍 BOOKING DETAIL
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_detail(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        tenant=request.user
    )

    serializer = BookingSerializer(booking)

    return Response(serializer.data)


# =========================
# ✏️ UPDATE BOOKING
# =========================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_booking(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        tenant=request.user
    )

    serializer = BookingSerializer(
        booking,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# =========================
# 🗑 DELETE BOOKING
# =========================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_booking(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        tenant=request.user
    )

    booking.delete()

    return Response({"message": "Deleted successfully"})

# Create your views here.
