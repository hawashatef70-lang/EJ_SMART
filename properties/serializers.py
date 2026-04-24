from rest_framework import serializers
from .models import Property, PropertyImage, PropertyVideo


# 🖼️ Property Images
class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']


# 🎥 Property Videos
class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = ['id', 'video']


# 🏠 Property Main Serializer
class PropertySerializer(serializers.ModelSerializer):

    images = PropertyImageSerializer(many=True, read_only=True)
    videos = PropertyVideoSerializer(many=True, read_only=True)

    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Property

        fields = [
            'id',
            'owner',
            'owner_username',
            'title',
            'description',
            'city',
            'address',
            'price',
            'property_type',
            'area',
            'bedrooms',
            'bathrooms',
            'is_available',
            'created_at',
            'images',
            'videos',
        ]

        read_only_fields = [
            'owner',
            'created_at',
            'owner_username'
        ]