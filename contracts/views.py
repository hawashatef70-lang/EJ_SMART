import base64

from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Contract, ContractSignature
from .serializers import ContractSerializer


# =========================
# 🔐 HELPER (reuse logic)
# =========================
def _get_contract_for_user(contract_id, user):
    contract = get_object_or_404(Contract, id=contract_id)

    if contract.booking.tenant != user:
        return None, Response({"error": "Not allowed"}, status=403)

    return contract, None


# =========================
# 📄 CONTRACT DETAIL
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_contract_detail(request, id):

    contract, error = _get_contract_for_user(id, request.user)
    if error:
        return error

    return Response(ContractSerializer(contract).data)


# =========================
# ✍️ SIGN CONTRACT
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_sign_contract(request, contract_id):

    contract, error = _get_contract_for_user(contract_id, request.user)
    if error:
        return error

    signature_data = request.data.get('signature_image')

    if not signature_data:
        return Response({"error": "No signature provided"}, status=400)

    try:
        format, imgstr = signature_data.split(';base64,')
        ext = format.split('/')[-1]

        file = ContentFile(
            base64.b64decode(imgstr),
            name=f'sign_{contract_id}.{ext}'
        )

        ContractSignature.objects.update_or_create(
            contract=contract,
            defaults={'signature_image': file, 'signed_by': request.user}
        )

        contract.signed = True
        contract.status = "signed"
        contract.save()

        return Response({"message": "Contract signed successfully"})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# =========================
# 📥 DOWNLOAD CONTRACT
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_download_contract(request, id):

    contract, error = _get_contract_for_user(id, request.user)
    if error:
        return error

    if not contract.contract_file:
        return Response({"error": "No file found"}, status=404)

    return Response({
        "file_url": contract.contract_file.url
    })


# =========================
# 📤 SEND CONTRACT
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_send_contract(request, id):

    contract, error = _get_contract_for_user(id, request.user)
    if error:
        return error

    contract.status = "sent"
    contract.save(update_fields=["status"])

    return Response({"message": "Contract sent successfully"})