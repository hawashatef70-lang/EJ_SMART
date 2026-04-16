from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Review
from properties.models import Property


def add_review(request, property_id):

    property = Property.objects.get(id=property_id)

    if request.method == "POST":

        rating = request.POST["rating"]

        comment = request.POST["comment"]

        Review.objects.create(

            user=request.user,

            property=property,

            rating=rating,

            comment=comment

        )

        return redirect("property_detail", id=property.id)

    return render(
        request,
        "reviews/add.html",
        {"property": property}
    )


def property_reviews(request, property_id):

    reviews = Review.objects.filter(property_id=property_id)

    return render(
        request,
        "reviews/list.html",
        {"reviews": reviews}
    )
# Create your views here.
