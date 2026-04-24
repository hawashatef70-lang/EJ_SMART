from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Favorite
from properties.models import Property
from .serializers import FavoriteSerializer


# =========================
# ❤️ TOGGLE FAVORITE (BEST PRACTICE)
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, property_id):

    prop = get_object_or_404(Property, id=property_id)

    favorite = Favorite.objects.filter(
        user=request.user,
        property=prop
    )

    # إذا موجود → احذفه
    if favorite.exists():
        favorite.delete()
        return Response({"message": "Removed from favorites"})

    # إذا مش موجود → أضفه
    Favorite.objects.create(
        user=request.user,
        property=prop
    )

    return Response({"message": "Added to favorites"})


# =========================
# 📄 LIST FAVORITES
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('property')

    serializer = FavoriteSerializer(favorites, many=True)

    return Response(serializer.data)


# =========================
# 🔍 FAVORITE DETAIL
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_detail(request, favorite_id):

    favorite = get_object_or_404(
        Favorite,
        id=favorite_id,
        user=request.user
    )

    serializer = FavoriteSerializer(favorite)

    return Response(serializer.data)


# =========================
# 🗑 CLEAR ALL FAVORITES
# =========================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_favorites(request):

    Favorite.objects.filter(user=request.user).delete()

    return Response({"message": "All favorites cleared"})
# Create your views here.
