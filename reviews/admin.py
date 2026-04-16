from django.contrib import admin
from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "property",
        "rating",
        "created_at"
    )
# Register your models here.
