from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class UserTypes(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        OWNER = 'owner', 'Owner'
        TENANT = 'tenant', 'Tenant'

    user_type = models.CharField(
        max_length=10,
        choices=UserTypes.choices,
        default=UserTypes.TENANT
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    national_id = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
# Create your models here.
