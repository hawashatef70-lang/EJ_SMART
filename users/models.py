from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER_TYPES = (
    ('', '----------'),  # القيمة الفاضية الأول، وبعدين الاسم اللي هيظهر
    ('admin', 'Admin'),
    ('owner', 'Owner'),
    ('tenant', 'Tenant'),
)

    user_type = models.CharField(
    max_length=10,
    choices=USER_TYPES,
    default='',    # كده هيفهم إن القيمة الافتراضية هي الفراغ اللي فوق
    null=True,     # مهمة جداً عشان قاعدة البيانات تقبل الفراغ ده
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
        null=True,
        blank=True
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
# Create your models here.
