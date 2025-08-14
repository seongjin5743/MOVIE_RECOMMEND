from django.db import models

class MovieReview(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    average_rating = models.FloatField()
    rating_sentiment = models.CharField(max_length=10)
    review_sentiment = models.CharField(max_length=10)
    overall_sentiment = models.CharField(max_length=10)

class MovieReviewText(models.Model):
    movie = models.ForeignKey(MovieReview, to_field='imdb_id', db_column='imdb_id', on_delete=models.CASCADE)
    review_title = models.TextField()
    review_rating = models.FloatField(null=True, blank=True)
    review_text = models.TextField()