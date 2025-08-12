import pandas as pd
from django.core.management.base import BaseCommand
from movies.models import MovieReviewText, MovieReview

import math

def safe_float(value):
    try:
        f = float(value)
        if math.isnan(f):
            return None
        return f
    except (ValueError, TypeError):
        return None

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        df = pd.read_csv("data/hadoop/dataset/imdb_reviews.csv", encoding="utf-8")
        df.columns = df.columns.str.strip()

        for _, row in df.iterrows():
            movie_review = MovieReview.objects.get(imdb_id=row['imdb_id'])

            MovieReviewText.objects.create(
                movie=movie_review,
                review_title=row['review title'],
                review_rating=safe_float(row.get('review_rating')),
                review_text=row['review']
            )
