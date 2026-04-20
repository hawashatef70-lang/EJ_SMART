from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from properties.models import Property
from bookings.models import Booking
from payments.models import Payment


@login_required
def dashboard(request):
    data = {
        "users": User.objects.count(),
        "properties": Property.objects.count(),
        "bookings": Booking.objects.count(),
        "payments": Payment.objects.count(),
    }
    return JsonResponse(data)


def search(request):
    properties = Property.objects.all()

    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if city:
        properties = properties.filter(city__icontains=city)

    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

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
def home(request):
    return JsonResponse({"message": "API is working"})
# Create your views here.
