from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer, RegisterSerializer
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

# ======================
# 🟢 REGISTER API
# ======================
@extend_schema(
    tags=["Users"],
    request=RegisterSerializer,
    responses={200: None}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response({
            "message": "User created successfully",
            "user_id": user.id
        })

    return Response(serializer.errors, status=400)


# ======================
# 🟢 LOGIN API
# ======================
@extend_schema(
    tags=["Users"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login success",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type,
                "is_verified": user.is_verified
            }
        })

    return Response({
        "error": "Invalid credentials"
    }, status=400)


# ======================
# 👤 PROFILE
# ======================
@extend_schema(
    tags=["Users"],
    responses=UserSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ======================
# ✏️ UPDATE PROFILE
# ======================
@extend_schema(
    tags=["Users"],
    request=UserSerializer,
    responses=UserSerializer
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):

    serializer = UserSerializer(
        request.user,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# ======================
# 🚪 LOGOUT API
# ======================
@extend_schema(
    tags=["Users"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):

    logout(request)
    return Response({"message": "Logged out successfully"})
# Create your views here.
