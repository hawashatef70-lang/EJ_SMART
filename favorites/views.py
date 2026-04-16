from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Favorite
from properties.models import Property

@login_required
def add_favorite(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    Favorite.objects.get_or_create(user=request.user, property=prop)
    return JsonResponse({"message": "Added to favorites"})


@login_required
def remove_favorite(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    Favorite.objects.filter(user=request.user, property=prop).delete()
    return JsonResponse({"message": "Removed"})


@login_required
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property')

    data = [
        {
            "id": f.property.id,
            "title": f.property.title,
            "price": f.property.price,
        }
        for f in favorites
    ]

    return JsonResponse(data, safe=False)





from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Favorite
from properties.models import Property
from .serializers import FavoriteSerializer

# ✅ إضافة للمفضلة
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_favorite(request, property_id):

    prop = get_object_or_404(Property, id=property_id)

    fav, created = Favorite.objects.get_or_create(
        user=request.user,
        property=prop
    )

    if not created:
        return Response({"message": "Already in favorites"})

    return Response({"message": "Added"})


# ✅ حذف من المفضلة
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_remove_favorite(request, property_id):

    prop = get_object_or_404(Property, id=property_id)

    Favorite.objects.filter(
        user=request.user,
        property=prop
    ).delete()

    return Response({"message": "Removed"})


# ✅ عرض المفضلة
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_list_favorites(request):

    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)

    return Response(serializer.data)
# Create your views here.
