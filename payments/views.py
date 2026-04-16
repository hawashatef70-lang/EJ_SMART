from django.shortcuts import render, redirect
from .models import Payment
from bookings.models import Booking


def make_payment(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    if request.method == "POST":

        method = request.POST["method"]

        Payment.objects.create(

            booking=booking,

            amount=booking.property.price,

            payment_method=method,

            status="completed"

        )

        return redirect("dashboard")

    return render(
        request,
        "payments/pay.html",
        {"booking": booking}
    )


def payment_list(request):

    payments = Payment.objects.all()

    return render(
        request,
        "payments/list.html",
        {"payments": payments}
    )
# =========================
# 🟢 API (NEW - CLEAN & SAFE)
# =========================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PaymentSerializer
from bookings.models import Booking


# 💳 API: Make Payment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_make_payment(request, booking_id):

    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)

    # 🔐 تأكد إن المستخدم صاحب الحجز
    if booking.tenant != request.user:
        return Response({"error": "Not allowed"}, status=403)

    serializer = PaymentSerializer(data=request.data)

    if serializer.is_valid():
        payment = serializer.save(
            booking=booking,
            amount=booking.property.price,
            status="completed"
        )
        return Response(PaymentSerializer(payment).data)

    return Response(serializer.errors, status=400)


# 📄 API: My Payments
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_payments(request):

    payments = Payment.objects.filter(booking__tenant=request.user)

    serializer = PaymentSerializer(payments, many=True)

    return Response(serializer.data)