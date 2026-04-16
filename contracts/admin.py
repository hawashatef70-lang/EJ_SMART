from django.contrib import admin
from django.utils.html import format_html
from .models import Contract, ContractSignature

# 1. إعداد شكل التوقيع ليظهر داخل صفحة العقد (Inline)
class SignatureInline(admin.StackedInline):
    model = ContractSignature
    extra = 1
    fields = ('signature_image', 'show_sig')
    readonly_fields = ('show_sig',)
    verbose_name = "توقيع العقد"
    verbose_name_plural = "توقيعات العقد"

    def show_sig(self, obj):
        if obj.signature_image:
            # عرض بريفيو للصورة في الأدمين
            return format_html('<img src="{}" width="200" style="border:1px solid #ccc; background:white; padding:5px; border-radius:5px;"/>', obj.signature_image.url)
        return "لا يوجد توقيع حالياً"
    show_sig.short_description = "معاينة التوقيع"

# 2. تسجيل العقد (Contract) وربطه بالتوقيع
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'signed') # تأكد أن هذه الحقول موجودة في موديل Contract
    inlines = [SignatureInline]

# ملاحظة هامة جداً: 
# لا تضف سطر admin.site.register(ContractSignature) أبداً 
# لكي لا يظهر التبويب المكرر الذي رأيته سابقاً.
# Register your models here.
