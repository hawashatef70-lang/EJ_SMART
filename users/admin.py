from django.contrib import admin
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "username",
        "email",
        "user_type",
        "phone",
        "is_verified"
    )
    # السطر اللي هيخليك تعدل "نوع المستخدم" و "التوثيق" من بره الجدول
    list_editable = ("user_type", "is_verified")

    # إضافة فلاتر على الجنب عشان تسهل عليك البحث
    list_filter = ("user_type", "is_verified")
    
    # السطر المعدل لإضافة التليفون والايميل
    list_editable = ("user_type", "is_verified", "phone", "email")
    
    # إضافة خانة بحث بالاسم أو الموبايل
    search_fields = ("username", "phone", "email")
# Register your models here.
