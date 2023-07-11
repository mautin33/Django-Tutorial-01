from django.contrib import admin

from watchlist.models import (
    StreamPlatform,
    WatchList,
    Review
)

# Register your models here.


class StreamPlatformAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


admin.site.register(StreamPlatform, StreamPlatformAdmin)


class WatchListAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


admin.site.register(WatchList, WatchListAdmin)


class ReviewAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


admin.site.register(Review, ReviewAdmin)
