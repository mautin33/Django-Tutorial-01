from django.urls import path 
from watchlist.views import (
    WatchListAV, 
    StreamPlatformAV,
    ReviewAV
)


urlpatterns = [
    path('movies/', WatchListAV.as_view(), name="movies"),
    path('streams/', StreamPlatformAV.as_view(), name="streams"),
    path('reviews/', ReviewAV.as_view(), name="reviews")
]

