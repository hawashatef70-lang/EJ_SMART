from django.db import models
from django.conf import settings  # ده الجوكر اللي بيجيب موديل المستخدم الصح
from properties.models import Property

class Favorite(models.Model):
    # ربط بـ settings.AUTH_USER_MODEL عشان يشتغل مع الـ Custom User بتاعك
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="favorites"
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} -> {self.property.title}"
# Create your models here.
