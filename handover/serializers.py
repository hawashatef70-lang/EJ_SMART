from rest_framework import serializers
from .models import Handover


class HandoverSerializer(serializers.ModelSerializer):

    property_title = serializers.CharField(source='property.title', read_only=True)
    tenant_name = serializers.CharField(source='tenant.username', read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Handover
        fields = [
            'id',
            'property',
            'property_title',
            'tenant',
            'tenant_name',
            'owner',
            'owner_name',
            'booking',
            'status',
            'is_confirmed_by_owner',
            'is_confirmed_by_tenant',
            'notes',
            'created_at'
        ]

        read_only_fields = [
            'id',
            'status',
            'created_at'
        ]