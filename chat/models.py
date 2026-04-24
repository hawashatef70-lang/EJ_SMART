from django.db import models
from users.models import User
from properties.models import Property


class Message(models.Model):

    # =========================
    # 👤 USERS
    # =========================
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    # =========================
    # 🏠 PROPERTY RELATION (IMPORTANT)
    # =========================
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="messages"
    )

    # =========================
    # 💬 MESSAGE CONTENT
    # =========================
    message = models.TextField()

    is_read = models.BooleanField(default=False)

    # =========================
    # ⏱ TIMESTAMP
    # =========================
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['receiver']),
            models.Index(fields=['property']),
        ]

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"
# Create your models here.
