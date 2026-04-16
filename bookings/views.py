from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Booking
from properties.models import Property


def create_booking(request, property_id):

    property = Property.objects.get(id=property_id)

    if request.method == "POST":

        start = request.POST['start_date']
        end = request.POST['end_date']

        Booking.objects.create(
            tenant=request.user,
            property=property,
            start_date=start,
            end_date=end
        )

        return redirect("dashboard")

    return render(request, "bookings/create.html", {"property": property})


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer
from properties.models import Property


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

    bookings = Booking.objects.filter(tenant=request.user)

    serializer = BookingSerializer(bookings, many=True)

    return Response(serializer.data)

# Create your views here.
