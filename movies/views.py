from django.shortcuts import render
from django.http import JsonResponse
from .models import MovieReview

import requests
from django.shortcuts import render
from .models import MovieReview

from django.conf import settings

OMDB_API_KEY = settings.OMDB_API_KEY


def movie_search(request):
    query = request.GET.get('q', '')
    movies = []
    posters = {}

    if query:
        movies = MovieReview.objects.filter(title__icontains=query)

        for movie in movies:
            url = f"https://www.omdbapi.com/?i={movie.imdb_id}&apikey={OMDB_API_KEY}"
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                posters[movie.imdb_id] = data.get('Poster')
            else:
                posters[movie.imdb_id] = None

    context = {
        'query': query,
        'movies': movies,
        'posters': posters,
    }
    return render(request, 'search.html', context)



def autocomplete_movies(request):
    query = request.GET.get('term', '')  # jQuery UI autocomplete는 기본이 'term'
    results = []
    if query:
        movies = MovieReview.objects.filter(title__icontains=query)[:10]  # 최대 10개
        results = list(movies.values_list('title', flat=True))
    return JsonResponse(results, safe=False)
