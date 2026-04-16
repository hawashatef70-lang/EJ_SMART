from django.db import models
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
        ('completed', 'Completed _ Success'),
        ('failed', 'Failed _ Canceled'),
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE
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

    transaction_id= models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Payment {self.id}"
# Create your models here.
