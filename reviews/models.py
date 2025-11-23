import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Review(models.Model):
    review_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.review_title)

    # From the tutorial
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    comment_author = models.CharField(max_length=100)
    comment_text = models.TextField()

    def __str__(self):
        return '(' + str(self.review) + ') ' + str(self.comment_author) + ": " + str(self.comment_text)

class File(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    path = models.CharField(max_length=1024)

    def __str__(self):
        return '(' + str(self.review) + ') ' + str(self.path)
