from django.db import models
from bookings.models import Booking


class Payment(models.Model):

    PAYMENT_METHODS = (
        ('card', 'Card'),
        ('wallet', 'Wallet'),
        ('bank', 'Bank Transfer'),
    )

    STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pending'
    )

    transaction_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.id} - {self.status}"
# Create your models here.
