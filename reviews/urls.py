from django.urls import path
from .views import *

urlpatterns = [

    path("add/<int:property_id>/", add_review, name="add_review"),

    path("property/<int:property_id>/", property_reviews, name="property_reviews"),

]