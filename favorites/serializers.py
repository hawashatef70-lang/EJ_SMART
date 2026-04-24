from rest_framework import serializers
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    # 🔥 تحسين عرض بيانات العقار بدل ما ترجع ID فقط
    property_title = serializers.CharField(source='property.title', read_only=True)
    property_price = serializers.DecimalField(
        source='property.price',
        max_digits=12,
        decimal_places=2,
        read_only=True
    )
    property_city = serializers.CharField(source='property.city', read_only=True)
    property_image = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = [
            'id',
            'property',
            'property_title',
            'property_price',
            'property_city',
            'property_image',
            'created_at'
        ]

        read_only_fields = [
            'id',
            'created_at'
        ]

    # 🖼️ أول صورة للعقار (لو موجودة)
    def get_property_image(self, obj):
        request = self.context.get('request')

        first_image = obj.property.images.first()
        if first_image and first_image.image:
            url = first_image.image.url
            return request.build_absolute_uri(url) if request else url

        return None