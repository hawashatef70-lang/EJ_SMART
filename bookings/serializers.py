from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):

    property_title = serializers.CharField(source='property.title', read_only=True)
    tenant_name = serializers.CharField(source='tenant.username', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'property',
            'property_title',
            'tenant',
            'tenant_name',
            'start_date',
            'end_date',
            'status',
            'created_at',
        ]

        read_only_fields = [
            'tenant',
            'status',
            'created_at'
        ]