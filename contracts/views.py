from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Contract, ContractSignature
from .serializers import ContractSerializer


# =========================
# ➕ CREATE CONTRACT
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_contract(request):

    serializer = ContractSerializer(data=request.data)

    if serializer.is_valid():
        contract = serializer.save()

        return Response({
            "message": "Contract created successfully",
            "data": ContractSerializer(contract).data
        })

    return Response(serializer.errors, status=400)


# =========================
# 📄 DETAIL CONTRACT
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_contract_detail(request, id):

    contract = get_object_or_404(Contract, id=id)

    return Response(ContractSerializer(contract).data)


# =========================
# ✏️ UPDATE CONTRACT
# =========================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_contract(request, id):

    contract = get_object_or_404(Contract, id=id)

    serializer = ContractSerializer(
        contract,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()

        return Response({
            "message": "Contract updated successfully",
            "data": serializer.data
        })

    return Response(serializer.errors, status=400)


# =========================
# 🗑 DELETE CONTRACT
# =========================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_contract(request, id):

    contract = get_object_or_404(Contract, id=id)
    contract.delete()

    return Response({"message": "Contract deleted successfully"})


# =========================
# ✍️ SIGN CONTRACT
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_sign_contract(request, id):

    contract = get_object_or_404(Contract, id=id)

    signature_data = request.data.get('signature_image')

    if not signature_data:
        return Response({"error": "No signature provided"}, status=400)

    ContractSignature.objects.update_or_create(
        contract=contract,
        defaults={
            "signature_image": signature_data,
            "signed_by": request.user
        }
    )

    contract.status = "signed"
    contract.save()

    return Response({"message": "Contract signed successfully"})


# =========================
# 📤 SEND CONTRACT
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_send_contract(request, id):

    contract = get_object_or_404(Contract, id=id)

    contract.status = "sent"
    contract.save()

    return Response({"message": "Contract sent successfully"})


# =========================
# 📥 DOWNLOAD CONTRACT
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_download_contract(request, id):

    contract = get_object_or_404(Contract, id=id)

    if not contract.contract_file:
        return Response({"error": "No file found"}, status=404)

    return Response({
        "file_url": contract.contract_file.url
    })