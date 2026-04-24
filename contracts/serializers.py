from rest_framework import serializers
from .models import Contract, ContractSignature


# =========================
# 📄 CONTRACT SERIALIZER
# =========================
class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


# =========================
# ✍️ CONTRACT SIGNATURE SERIALIZER
# =========================
class ContractSignatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractSignature
        fields = '__all__'
        read_only_fields = ('signed_at',)