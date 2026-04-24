from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

from properties.models import Property
from bookings.models import Booking
from payments.models import Payment


User = get_user_model()


# =========================
# 🏠 HOME
# =========================
def home(request):
    return JsonResponse({
        "status": "ok",
        "message": "EJ_SMART API is running"
    })


# =========================
# 📊 DASHBOARD
# =========================
@login_required
def dashboard(request):

    data = {
        "users": User.objects.count(),
        "properties": Property.objects.count(),
        "bookings": Booking.objects.count(),
        "payments": Payment.objects.count(),
    }

    return JsonResponse(data)


# =========================
# 🔍 SEARCH
# =========================
def search(request):

    properties = Property.objects.all()

    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    filters = Q()

    if city:
        filters &= Q(city__icontains=city)

    if min_price:
        filters &= Q(price__gte=min_price)

    if max_price:
        filters &= Q(price__lte=max_price)

    properties = properties.filter(filters)

    data = [
        {
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "city": p.city,
        }
        for p in properties
    ]

    return JsonResponse(data, safe=False)
# Create your views here.
