import base64
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Contract, ContractSignature
from .serializers import ContractSerializer


# =========================
# 🟦 WEB (OLD)
# =========================

def contract_detail(request, id):
    contract = get_object_or_404(Contract, id=id)
    return render(request, "contracts/detail.html", {"contract": contract})


@csrf_exempt
def save_contract_signature(request, contract_id):

    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    try:
        signature_data = request.POST.get('signature_image')

        if not signature_data:
            return JsonResponse({'status': 'error', 'message': 'No data'}, status=400)

        format, imgstr = signature_data.split(';base64,')
        ext = format.split('/')[-1]

        file = ContentFile(
            base64.b64decode(imgstr),
            name=f'sig_{contract_id}.{ext}'
        )

        contract = get_object_or_404(Contract, id=contract_id)

        ContractSignature.objects.update_or_create(
            contract=contract,
            defaults={'signature_image': file}
        )

        contract.signed = True
        contract.status = "signed"
        contract.save()

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# =========================
# 🟢 API
# =========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_contract_detail(request, id):

    contract = get_object_or_404(Contract, id=id)

    # 🔐 حماية
    if contract.booking.tenant != request.user:
        return Response({"error": "Not allowed"}, status=403)

    return Response(ContractSerializer(contract).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_sign_contract(request, contract_id):

    contract = get_object_or_404(Contract, id=contract_id)

    # 🔐 حماية
    if contract.booking.tenant != request.user:
        return Response({"error": "Not allowed"}, status=403)

    signature_data = request.data.get('signature_image')

    if not signature_data:
        return Response({"error": "No signature"}, status=400)

    try:
        format, imgstr = signature_data.split(';base64,')
        ext = format.split('/')[-1]

        file = ContentFile(
            base64.b64decode(imgstr),
            name=f'sign_{contract_id}.{ext}'
        )

        ContractSignature.objects.update_or_create(
            contract=contract,
            defaults={'signature_image': file}
        )

        contract.signed = True
        contract.status = "signed"
        contract.save()

        return Response({"message": "Signed successfully"})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_download_contract(request, id):

    contract = get_object_or_404(Contract, id=id)

    if contract.booking.tenant != request.user:
        return Response({"error": "Not allowed"}, status=403)

    if not contract.contract_file:
        return Response({"error": "No file"}, status=404)

    return Response({
        "file_url": contract.contract_file.url
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_send_contract(request, id):

    contract = get_object_or_404(Contract, id=id)

    # 🔐 حماية
    if contract.booking.tenant != request.user:
        return Response({"error": "Not allowed"}, status=403)

    contract.status = "sent"
    contract.save()

    return Response({"message": "Contract sent"})