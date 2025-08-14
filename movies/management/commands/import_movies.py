import pandas as pd
from django.core.management.base import BaseCommand
from movies.models import MovieReview

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        df = pd.read_csv("data/sentiment_movie_rates.csv", encoding='utf-8')
        df.columns = df.columns.str.strip()

        for _, row in df.iterrows():
            MovieReview.objects.create(
                imdb_id=row['IMDB_ID'],
                title=row['Title'],
                average_rating=float(row['Average_Rating']),
                rating_sentiment=row['Rating_Sentiment'],
                review_sentiment=row['Review_Sentiment'],
                overall_sentiment=row['Overall_Sentiment']
            )