from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Property, PropertyImage, PropertyVideo
from .serializers import PropertySerializer
from drf_spectacular.utils import extend_schema
import traceback

# =====================================================
# 🟦 WEB (OPTIONAL - KEEP IF YOU STILL NEED HTML)
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

    return render(request, "properties/list.html", {"properties": properties})


def property_detail(request, id):
    prop = get_object_or_404(Property, id=id)

    return render(request, "properties/detail.html", {
        "property": prop,
        "images": prop.images.all(),
        "videos": prop.videos.all()
    })


@login_required
def create_property(request):
    if request.user.user_type != 'owner' or not request.user.is_verified:
        messages.error(request, "غير مسموح لك بإضافة عقارات")
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
# 🟢 API HELPERS
# =====================================================

def apply_filters(request, queryset):

    q = request.GET.get('q')
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(city__icontains=q) |
            Q(address__icontains=q)
        )

    city = request.GET.get('city')
    if city:
        queryset = queryset.filter(city__icontains=city)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    property_type = request.GET.get('property_type')
    if property_type:
        queryset = queryset.filter(property_type=property_type)

    is_available = request.GET.get('is_available')
    if is_available:
        queryset = queryset.filter(is_available=is_available.lower() == 'true')

    return queryset


# =====================================================
# 🟢 API - LIST
# =====================================================

@extend_schema(tags=["Properties"])
@api_view(['GET'])
@permission_classes([AllowAny])
def api_properties(request):

    properties = Property.objects.all()
    properties = apply_filters(request, properties)

    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


# =====================================================
# 🟢 API - DETAIL
# =====================================================

@extend_schema(tags=["Properties"])
@api_view(['GET'])
@permission_classes([AllowAny])
def api_property_detail(request, id):

    prop = get_object_or_404(Property, id=id)
    serializer = PropertySerializer(prop)
    return Response(serializer.data)


# =====================================================
# 🟢 API - CREATE
# =====================================================

@extend_schema(tags=["Properties"])
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


# =====================================================
# 🟢 API - UPDATE
# =====================================================

@extend_schema(tags=["Properties"])
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_property(request, id):

    prop = get_object_or_404(Property, id=id)

    serializer = PropertySerializer(prop, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# =====================================================
# 🟢 API - DELETE
# =====================================================

@extend_schema(tags=["Properties"])
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_property(request, id):

    prop = get_object_or_404(Property, id=id)
    prop.delete()

    return Response({"message": "Deleted successfully"})