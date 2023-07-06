from django.urls import path 
from watchlist__app.api.views import MovieList, MovieDetail


urlpatterns = [
    path('movies/', MovieList.as_view(), name="movies"),
    path('movie/<uuid:id>/', MovieDetail.as_view(), name="movie-detail")
]


