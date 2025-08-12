from django.db import models

class MovieReview(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    average_rating = models.FloatField()
    rating_sentiment = models.CharField(max_length=10)
    review_sentiment = models.CharField(max_length=10)
    overall_sentiment = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.title} ({self.imdb_id})"
