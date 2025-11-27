from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Review

def comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.comment_set.create(comment_author=request.POST["author"], comment_text=request.POST["comment"])
    return HttpResponseRedirect(reverse("reviews:detail", args=(review.id,)))

class IndexView(generic.ListView):
    template_name = "reviews/index.html"

    def get_queryset(self):
        return Review.objects.order_by("-pub_date")

class DetailView(generic.DetailView):
    model = Review
    template_name = "reviews/detail.html"
