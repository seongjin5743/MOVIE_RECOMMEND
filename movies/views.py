from django.shortcuts import render
from django.http import JsonResponse
from .models import MovieReview
import random
import requests
from django.shortcuts import render
from .models import MovieReview, MovieReviewText

from django.conf import settings

OMDB_API_KEY = settings.OMDB_API_KEY

def movie_search(request):
    query = request.GET.get('q', '')
    movies = []
    posters = {}
    selected_reviews = {}

    if query:
        movies = MovieReview.objects.filter(title__icontains=query)

        for movie in movies:
            # OMDB 포스터 요청
            url = f"https://www.omdbapi.com/?i={movie.imdb_id}&apikey={OMDB_API_KEY}"
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                posters[movie.imdb_id] = data.get('Poster')
            else:
                posters[movie.imdb_id] = None

            overall = movie.overall_sentiment.lower()
            reviews_qs = MovieReviewText.objects.filter(movie=movie)

            if overall == 'positive' or overall == '긍정':
                reviews_qs = reviews_qs.filter(review_rating__gte=7)
            elif overall == 'negative' or overall == '부정':
                reviews_qs = reviews_qs.filter(review_rating__lte=5)
            elif overall == 'neutral' or overall == '호불호':

                pos_reviews = reviews_qs.filter(review_rating__gte=7)
                neg_reviews = reviews_qs.filter(review_rating__lte=5)
                reviews_qs = list(pos_reviews) + list(neg_reviews)
            else:
                reviews_qs = list(reviews_qs)

            if reviews_qs:
                if isinstance(reviews_qs, list):
                    selected_review = random.choice(reviews_qs)
                else:
                    count = reviews_qs.count()
                    random_index = random.randint(0, count - 1)
                    selected_review = reviews_qs[random_index]
                selected_reviews[movie.imdb_id] = selected_review
            else:
                selected_reviews[movie.imdb_id] = None

    context = {
        'query': query,
        'movies': movies,
        'posters': posters,
        'selected_reviews': selected_reviews,
    }
    return render(request, 'search.html', context)



def autocomplete_movies(request):
    query = request.GET.get('term', '')
    results = []
    if query:
        movies = MovieReview.objects.filter(title__icontains=query)[:10]
        results = list(movies.values_list('title', flat=True))
    return JsonResponse(results, safe=False)
