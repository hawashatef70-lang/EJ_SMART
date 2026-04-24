from django.shortcuts import get_object_or_404
from django.db.models import Avg

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Review
from .serializers import ReviewSerializer
from properties.models import Property


# =========================
# 🟢 ADD REVIEW (API)
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, property_id):

    property_obj = get_object_or_404(Property, id=property_id)

    rating = request.data.get("rating")
    comment = request.data.get("comment")

    if not rating or not comment:
        return Response({"error": "rating and comment are required"}, status=400)

    # optional: منع تكرار review
    if Review.objects.filter(user=request.user, property=property_obj).exists():
        return Response({"error": "You already reviewed this property"}, status=400)

    review = Review.objects.create(
        user=request.user,
        property=property_obj,
        rating=rating,
        comment=comment
    )

    return Response(ReviewSerializer(review).data)


# =========================
# 📄 PROPERTY REVIEWS
# =========================
@api_view(['GET'])
def property_reviews(request, property_id):

    property_obj = get_object_or_404(Property, id=property_id)

    reviews = Review.objects.filter(property=property_obj)

    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']

    serializer = ReviewSerializer(reviews, many=True)

    return Response({
        "average_rating": avg_rating or 0,
        "count": reviews.count(),
        "reviews": serializer.data
    })
# Create your views here.
