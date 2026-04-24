from django.db import models
from django.conf import settings


class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ('system', 'System'),
        ('booking', 'Booking'),
        ('payment', 'Payment'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=255, default="Notification")
    message = models.TextField()

    type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='system'
    )

    is_read = models.BooleanField(default=False)

    reference_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.user} - {self.title}"
# Create your models here.
