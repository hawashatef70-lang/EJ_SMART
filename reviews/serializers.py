from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source='user.username', read_only=True)
    property_title = serializers.CharField(source='property.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'user_name',
            'property',
            'property_title',
            'rating',
            'comment',
            'created_at'
        ]

        read_only_fields = ['user', 'created_at']