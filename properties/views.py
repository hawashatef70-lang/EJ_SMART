from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Property, PropertyImage, PropertyVideo
from .serializers import PropertySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# =====================================================
# 🟦 WEB VIEWS (OLD - KEEP AS IS)
# =====================================================

def property_list(request):
    properties = Property.objects.all()

    q = request.GET.get('q')
    if q:
        properties = properties.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(city__icontains=q) |
            Q(address__icontains=q)
        )

    city = request.GET.get('city')
    if city:
        properties = properties.filter(city__icontains=city)

    p_type = request.GET.get('property_type')
    if p_type:
        properties = properties.filter(property_type=p_type)

    available = request.GET.get('is_available')
    if available:
        is_avail_bool = True if available.lower() == 'true' else False
        properties = properties.filter(is_available=is_avail_bool)
    else:
        properties = properties.filter(is_available=True)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    min_area = request.GET.get('min_area')
    max_area = request.GET.get('max_area')

    if min_area:
        properties = properties.filter(area__gte=min_area)
    if max_area:
        properties = properties.filter(area__lte=max_area)

    bedrooms = request.GET.get('bedrooms')
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)

    bathrooms = request.GET.get('bathrooms')
    if bathrooms:
        properties = properties.filter(bathrooms=bathrooms)

    sort_by = request.GET.get('sort_by')

    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'area_asc': 'area',
        'area_desc': '-area',
        'newest': '-created_at'
    }

    properties = properties.order_by(sort_options.get(sort_by, '-created_at'))

    return render(request, "properties/list.html", {"properties": properties})


def property_detail(request, id):
    property = get_object_or_404(Property, id=id)

    return render(request, "properties/detail.html", {
        "property": property,
        "images": property.images.all(),
        "videos": property.videos.all()
    })


@login_required
def create_property(request):
    if request.user.user_type != 'owner' or not request.user.is_verified:
        messages.error(request, "عذراً، يجب توثيق حسابك كمالك.")
        return redirect('property_list')

    if request.method == "POST":
        prop = Property.objects.create(
            owner=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            city=request.POST.get("city"),
            address=request.POST.get("address"),
            price=request.POST.get("price") or 0,
            property_type=request.POST.get("property_type"),
            area=request.POST.get("area") or 0,
            bedrooms=request.POST.get("bedrooms") or 1,
            bathrooms=request.POST.get("bathrooms") or 1
        )

        for img in request.FILES.getlist("images"):
            PropertyImage.objects.create(property=prop, image=img)

        for vid in request.FILES.getlist("videos"):
            PropertyVideo.objects.create(property=prop, video=vid)

        messages.success(request, "تم إضافة العقار بنجاح!")
        return redirect("property_list")


# =====================================================
# 🟢 API VIEWS (NEW)
# =====================================================

@api_view(['GET'])
def api_properties(request):

    properties = Property.objects.all()

    q = request.GET.get('q')
    if q:
        properties = properties.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(city__icontains=q) |
            Q(address__icontains=q)
        )

    city = request.GET.get('city')
    if city:
        properties = properties.filter(city__icontains=city)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_property_detail(request, id):

    try:
        prop = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)

    serializer = PropertySerializer(prop)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_property(request):

    serializer = PropertySerializer(data=request.data)

    if serializer.is_valid():
        property_obj = serializer.save(owner=request.user)

        for img in request.FILES.getlist('images'):
            PropertyImage.objects.create(property=property_obj, image=img)

        for vid in request.FILES.getlist('videos'):
            PropertyVideo.objects.create(property=property_obj, video=vid)

        return Response(PropertySerializer(property_obj).data)

    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def api_update_property(request, id):
    try:
        prop = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)

    serializer = PropertySerializer(prop, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def api_delete_property(request, id):
    try:
        prop = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)

    prop.delete()
    return Response({"message": "Deleted successfully"})