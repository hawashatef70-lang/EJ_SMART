from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Handover
from bookings.models import Booking


# =========================
# 🟦 CREATE HANDOVER
# =========================

def create_handover(request, booking_id):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    booking = get_object_or_404(Booking, id=booking_id)

    # 🔐 حماية
    if request.user != booking.tenant and request.user != booking.property.owner:
        return JsonResponse({"error": "Not allowed"}, status=403)

    # منع التكرار
    if Handover.objects.filter(booking=booking).exists():
        return JsonResponse({"error": "Already exists"}, status=400)

    handover = Handover.objects.create(
        property=booking.property,
        tenant=booking.tenant,
        owner=booking.property.owner,
        booking=booking
    )

    return JsonResponse({
        "message": "Handover created",
        "handover_id": handover.id
    })


# =========================
# 🟦 CONFIRM HANDOVER
# =========================

def confirm_handover(request, handover_id):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    handover = get_object_or_404(Handover, id=handover_id)

    # 🔐 حماية
    if request.user not in [handover.owner, handover.tenant]:
        return JsonResponse({"error": "Not allowed"}, status=403)

    if request.user == handover.owner:
        handover.is_confirmed_by_owner = True

    if request.user == handover.tenant:
        handover.is_confirmed_by_tenant = True

    if handover.is_confirmed_by_owner and handover.is_confirmed_by_tenant:
        handover.status = "completed"

    handover.save()

    return JsonResponse({
        "message": "Handover updated",
        "status": handover.status
    })


# =========================
# 🟦 MY HANDOVERS
# =========================

def my_handovers(request):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    handovers = Handover.objects.filter(
        Q(owner=request.user) | Q(tenant=request.user)
    )

    data = [
        {
            "id": h.id,
            "property": str(h.property),
            "status": h.status,
            "is_owner_confirmed": h.is_confirmed_by_owner,
            "is_tenant_confirmed": h.is_confirmed_by_tenant,
            "created_at": h.created_at
        }
        for h in handovers
    ]

    return JsonResponse({"handovers": data})
# Create your views here.
