from django.db import models
from bookings.models import Booking


# =========================
# 📄 CONTRACT MODEL
# =========================
class Contract(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('signed', 'Signed'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="contract"
    )

    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateField()
    end_date = models.DateField()

    contract_file = models.FileField(upload_to="contracts/")

    signed = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['booking']),
        ]

    def __str__(self):
        return f"Contract #{self.id} - Booking #{self.booking.id}"


# =========================
# ✍️ CONTRACT SIGNATURE MODEL
# =========================
class ContractSignature(models.Model):

    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        related_name='signature'
    )

    signature_image = models.ImageField(
        upload_to='signatures/%Y/%m/',
        null=True,
        blank=True
    )

    signed_at = models.DateTimeField(auto_now_add=True)

    signed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-signed_at']

    def __str__(self):
        return f"Signature - Contract #{self.contract.id}"