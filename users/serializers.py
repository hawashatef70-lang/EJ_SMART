from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'phone',
            'national_id',
            'profile_image',
            'user_type',
            'is_verified',
            'created_at',
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'national_id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'phone',
            'user_type',
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            user_type=validated_data.get('user_type', 'tenant')
        )
        return user