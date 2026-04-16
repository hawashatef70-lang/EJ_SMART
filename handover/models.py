from django.db import models
from users.models import User
from properties.models import Property
from bookings.models import Booking

class Handover(models.Model):

    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_handover')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_handover')

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    is_confirmed_by_owner = models.BooleanField(default=False)
    is_confirmed_by_tenant = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
        ],
        default='pending'
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Handover - {self.property}"

# Create your models here.
