from django.db import models
from helper.basemodel import BaseModel

# Create your models here.

class Movie(BaseModel):
    name =  models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name 
    
    