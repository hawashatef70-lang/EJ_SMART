from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Property
from .serializers import PropertySerializer


# =========================
# 🟢 LIST + CREATE
# =========================
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def api_properties(request):

    # GET → كل العقارات
    if request.method == "GET":
        q = request.GET.get('q')

        properties = Property.objects.all()

        if q:
            properties = properties.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(city__icontains=q) |
                Q(address__icontains=q)
            )

        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

    # POST → إضافة عقار
    elif request.method == "POST":
        serializer = PropertySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


# =========================
# 🟢 DETAIL + UPDATE + DELETE
# =========================
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def api_property_detail(request, id):

    prop = get_object_or_404(Property, id=id)

    # GET → تفاصيل
    if request.method == "GET":
        serializer = PropertySerializer(prop)
        return Response(serializer.data)

    # PUT → تعديل
    elif request.method == "PUT":
        serializer = PropertySerializer(prop, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # DELETE → حذف
    elif request.method == "DELETE":
        prop.delete()
        return Response({"message": "Deleted successfully"})