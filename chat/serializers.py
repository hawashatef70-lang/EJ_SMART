from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):

    # =========================
    # 👤 DISPLAY FIELDS
    # =========================
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    receiver_name = serializers.CharField(source='receiver.username', read_only=True)

    # =========================
    # 🏠 PROPERTY INFO (instead of raw ID)
    # =========================
    property_title = serializers.CharField(source='property.title', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receiver',
            'sender_name',
            'receiver_name',
            'message',

            # 🔥 improved relation instead of property_id
            'property',
            'property_title',

            'is_read',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'sender_name',
            'receiver_name',
            'property_title',
            'created_at',
        ]