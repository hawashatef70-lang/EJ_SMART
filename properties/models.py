from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Property(models.Model):

    PROPERTY_TYPES = (
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('supermarket', 'Supermarket'),
        ('restaurant', 'Restaurant'),
        ('grocery_store', 'Grocery Store'),
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_properties'
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    property_type = models.CharField(
        max_length=50,
        choices=PROPERTY_TYPES,
        default='apartment'
    )

    area = models.FloatField(default=0.0)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.owner}"


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="properties/images/")

    def __str__(self):
        return f"Image for {self.property.title}"


class PropertyVideo(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="videos"
    )
    video = models.FileField(upload_to="properties/videos/")

    def __str__(self):
        return f"Video for {self.property.title}"