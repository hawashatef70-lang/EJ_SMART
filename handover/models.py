from django.db import models
from users.models import User
from properties.models import Property
from bookings.models import Booking


class Handover(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="handovers"
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="handovers"
    )

    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tenant_handovers'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_handovers'
    )

    is_confirmed_by_owner = models.BooleanField(default=False)
    is_confirmed_by_tenant = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    notes = models.TextField(blank=True, null=True)

    # 🔥 tracking مهم جدًا
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['property']),
            models.Index(fields=['booking']),
        ]

    def __str__(self):
        return f"Handover #{self.id} - {self.property}"

# Create your models here.
