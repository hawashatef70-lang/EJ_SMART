from django.db import models
from django.db import models
from django.conf import settings
from properties.models import Property

User = settings.AUTH_USER_MODEL


class Booking(models.Model):

    tenant = models.ForeignKey(User, on_delete=models.CASCADE)

    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(max_length=20, default="pending")
    status = models.CharField(
    max_length=20,
    choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ],
    default='pending'
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.property} - {self.tenant}"
# Create your models here.
