from rest_framework import serializers

from watchlist.models import (
    WatchList, 
    StreamPlatform, 
    Review
)


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["watch_list"]
        

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"
        read_only_fields = ["platform"]


class StreamPlatformSerializer(serializers.ModelSerializer):
    # watch_list = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"
