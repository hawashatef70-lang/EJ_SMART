from rest_framework import serializers
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)
    property_price = serializers.DecimalField(source='property.price', max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Favorite
        fields = [
            'id',
            'property',
            'property_title',
            'property_price'
        ]