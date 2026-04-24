from django.shortcuts import render, redirect
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer
from properties.models import Property


# =========================
# 🟦 WEB (OPTIONAL - LEGACY)
# =========================
def create_booking(request, property_id):

    property = Property.objects.get(id=property_id)

    if request.method == "POST":

        Booking.objects.create(
            tenant=request.user,
            property=property,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date')
        )

        return redirect("dashboard")

    return render(request, "bookings/create.html", {"property": property})


# =========================
# 📅 CREATE BOOKING API
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_booking(request, property_id):

    try:
        property = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)

    serializer = BookingSerializer(data=request.data)

    if serializer.is_valid():

        with transaction.atomic():
            booking = serializer.save(
                tenant=request.user,
                property=property
            )

        return Response(BookingSerializer(booking).data)

    return Response(serializer.errors, status=400)


# =========================
# 📄 MY BOOKINGS API
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bookings(request):

    bookings = Booking.objects.filter(tenant=request.user).select_related('property')

    serializer = BookingSerializer(bookings, many=True)

    return Response(serializer.data)

# Create your views here.
