from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

# 1. دالة التسجيل: المالك بيسجل بياناته ويحدد نوعه بنفسه
def register(request):
    if request.method == "POST":
        # استخدام .get للحماية من الأخطاء لو حقل فاضي
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        user_type = request.POST.get("user_type")

        # إنشاء المستخدم (is_verified بيفضل False تلقائياً)
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            user_type=user_type
        )
        
        # رسالة تظهر للمالك بعد التسجيل عشان يعرف إنه مستني الأدمن
        messages.success(request, "تم التسجيل بنجاح! حسابك قيد المراجعة من قبل الإدارة.")
        return redirect("login")

    return render(request, "users/register.html")

# 2. دالة تسجيل الدخول
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "خطأ في اسم المستخدم أو كلمة المرور")

    return render(request, "users/login.html")

# 3. الداشبورد: اللي بيفصل بين "الموثق" و "قيد الانتظار"
def dashboard(request):
    # حماية الصفحة: لو مش عامل لوجين يرجعه لصفحة اللوجين
    if not request.user.is_authenticated:
        return redirect("login")
        
    user = request.user
    context = {
        'user': user,
        'is_owner': user.user_type == 'owner',
        'is_verified': user.is_verified, # القيمة دي بتتغير لـ True لما الأدمن يوافق من الـ Admin Panel
    }
    return render(request, "users/dashboard.html", context)

# 4. تسجيل الخروج
def logout_view(request):
    logout(request)
    return redirect("login")


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer, RegisterSerializer

# ======================
# 🟢 REGISTER
# ======================
@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response({
            "message": "User created",
            "user_id": user.id
        })

    return Response(serializer.errors, status=400)


# ======================
# 🟢 LOGIN (FIXED)
# ======================
@api_view(['POST'])
def api_login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        return Response({
            "message": "Login success",
            "user_id": user.id,
            "username": user.username,
            "user_type": user.user_type,
            "is_verified": user.is_verified
        })

    return Response({"error": "Invalid credentials"}, status=400)


# ======================
# 👤 PROFILE (GET)
# ======================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ======================
# ✏️ UPDATE PROFILE
# ======================
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
# Create your views here.
