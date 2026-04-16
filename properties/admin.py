from django.contrib import admin
from .models import Property, PropertyImage, PropertyVideo

# 1. نظام رفع الصور المدمج
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 2
    fields = ['image']

# 2. نظام رفع الفيديوهات المدمج
class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 1
    fields = ['video']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # --- 1. الجدول الرئيسي ---
    list_display = (
        'title', 
        'owner', 
        'property_type', 
        'city', 
        'price', 
        'area', # أضفنا المساحة للجدول
        'is_available', 
        'created_at'
    )

    # --- 2. التعديل السريع من الخارج ---
    list_editable = ('price', 'is_available', 'property_type')

    # --- 3. الفلاتر (الخانات اللي فوق وفي الجنب) ---
    # ملاحظة: دجانغو هيظهرbedrooms و bathrooms كخانات اختيار فوق
    # والسعر والمساحة هيظهروا في القائمة الجانبية كفلاتر ذكية
    list_filter = (
        'is_available', 
        'property_type', 
        'city', 
        'bedrooms', 
        'bathrooms',
        'price',  # إضافة البحث/الفلترة بالسعر
        'area',   # إضافة البحث/الفلترة بالمساحة
    )

    # --- 4. خانة البحث النصي ---
    search_fields = ('title', 'owner__username', 'city', 'address')

    # --- 5. تقسيم صفحة الإدخال (Fieldsets) ---
    fieldsets = (
        ("المعلومات الأساسية", {
            'fields': ('owner', 'title', 'description', 'property_type')
        }),
        ("الموقع بالتفصيل", {
            'fields': ('city', 'address')
        }),
        ("المواصفات الفنية والمالية", {
            'fields': ('price', 'area', 'bedrooms', 'bathrooms', 'is_available')
        }),
    )

    inlines = [PropertyImageInline, PropertyVideoInline]
    ordering = ('-created_at',)

# تسجيل الميديا بشكل منفصل للإدارة السريعة
admin.site.register(PropertyImage)
admin.site.register(PropertyVideo)