from django.db import models
from django.conf import settings
from properties.models import Property
from django.utils import timezone


class Favorite(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    # 🔥 مهم جدًا للتتبع
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'property')

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['property']),
        ]

    def __str__(self):
        return f"{self.user.username} ❤️ {self.property.title}"
# Create your models here.
