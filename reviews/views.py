from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.template import loader

from .models import Review

# Create your views here.
def index(request):
    review_list = Review.objects.order_by("-pub_date")
    context = {"review_list": review_list}
    return render(request, "polls/index.html", context)

def detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    comments = review.comment_set.all()
    return render(request, "reviews/detail.html", {"review":review, "comment_list":comments})

