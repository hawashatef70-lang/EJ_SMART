from django.db import models
from django.conf import settings # ده البديل الصح لـ User

class Notification(models.Model):
    # ربط بـ settings.AUTH_USER_MODEL عشان يشتغل مع الـ Custom User بتاعك
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="notifications"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # بنستخدم self.user.username عادي جداً في العرض
        return f"Notification for {self.user.username}"
# Create your models here.
