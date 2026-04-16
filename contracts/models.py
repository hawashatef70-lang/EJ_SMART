from django.db import models
from bookings.models import Booking

# 1. موديل العقد
class Contract(models.Model):

    STATUS = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('signed', 'Signed'),
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        verbose_name="Booking"
    )

    rent_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Rent Amount"
    )

    deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Deposit"
    )

    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")

    contract_file = models.FileField(
        upload_to="contracts/",
        verbose_name="Contract File"
    )

    signed = models.BooleanField(default=False, verbose_name="Signed")

    # ✅ الصح هنا
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='draft'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    def __str__(self):
        return f"Contract {self.id} - Booking {self.booking.id}"

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"


# 2. موديل التوقيع
class ContractSignature(models.Model):

    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        related_name='signature_info',
        verbose_name="Contract"
    )

    signature_image = models.ImageField(
        upload_to='signatures/%Y/%m/',
        null=True,
        blank=True,
        verbose_name="Signature Image"
    )

    signed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Signed At"
    )

    def __str__(self):
        return f"Signature for Contract {self.contract.id}"

    class Meta:
        verbose_name = "Contract Signature"
        verbose_name_plural = "Contract Signatures"