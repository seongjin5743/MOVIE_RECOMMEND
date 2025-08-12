from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_search, name='home'),  # 루트 URL → 검색 페이지
    path('autocomplete/', views.autocomplete_movies, name='autocomplete_movies'),  # 자동완성 API
]
