from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer
from bookings.models import Booking
from drf_spectacular.utils import extend_schema

# =====================================================
# 🟢 CREATE PAYMENT (API ONLY)
# =====================================================

@extend_schema(tags=["Payments"])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_make_payment(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    # 🔐 Ownership check
    if booking.tenant != request.user:
        return Response({"error": "Not allowed"}, status=403)

    # 💰 prevent duplicate payment
    if Payment.objects.filter(booking=booking, status="completed").exists():
        return Response({"error": "Already paid"}, status=400)

    serializer = PaymentSerializer(data=request.data)

    if serializer.is_valid():

        payment = serializer.save(
            booking=booking,
            amount=booking.property.price,
            status="completed"
        )

        return Response({
            "message": "Payment successful",
            "payment": PaymentSerializer(payment).data
        })

    return Response(serializer.errors, status=400)


# =====================================================
# 🟢 MY PAYMENTS
# =====================================================

@extend_schema(tags=["Payments"])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_payments(request):

    payments = Payment.objects.filter(booking__tenant=request.user)

    serializer = PaymentSerializer(payments, many=True)

    return Response(serializer.data)


# =====================================================
# 🟢 PAYMENT DETAIL (OPTIONAL BUT IMPORTANT)
# =====================================================

@extend_schema(tags=["Payments"])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_detail(request, payment_id):

    payment = get_object_or_404(Payment, id=payment_id)

    # 🔐 security
    if payment.booking.tenant != request.user:
        return Response({"error": "Not allowed"}, status=403)

    serializer = PaymentSerializer(payment)

    return Response(serializer.data)

# ✏️ UPDATE PAYMENT
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_payment(request, payment_id):

    payment = get_object_or_404(Payment, id=payment_id)

    # 🔐 check owner
    if payment.booking.tenant != request.user:
        return Response({"error": "Not allowed"}, status=403)

    serializer = PaymentSerializer(payment, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# 🗑 DELETE PAYMENT
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_payment(request, payment_id):

    payment = get_object_or_404(Payment, id=payment_id)

    # 🔐 check owner
    if payment.booking.tenant != request.user:
        return Response({"error": "Not allowed"}, status=403)

    payment.delete()

    return Response({"message": "Payment deleted"})