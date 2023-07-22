from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from helper.basemodel import BaseModel

# Create your models here.


class StreamPlatform(BaseModel):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    class Meta:
        verbose_name = _("StreamPlatform")
        verbose_name_plural = _("StreamPlatforms")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class WatchList(BaseModel):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    platform = models.ForeignKey(
        StreamPlatform, on_delete=models.CASCADE, related_name="watch_list")

    class Meta:
        verbose_name = _("WatchList")
        verbose_name_plural = _("WatchLists")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Review(BaseModel):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    watch_list = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ["-created_at"]    
 
    def __str__(self):
        return f"{str(self.rating)} || {self.description[:10]}"
    
    # @classmethod
    # def update_review(
    #     cls,
    #     id: str,
    #     rating: int = None
    # ):
    #     review = cls.objects.filter(id=id).last()
    #     if review is not None: 
    #         pass 
    #     return None 
        
    
    
    
    
    
    
    