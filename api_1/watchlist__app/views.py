from django.shortcuts import render
from django_seed import Seed
from random import randint
from django.utils import timezone

from watchlist__app.models import Movie

# Create your views here.

now = timezone.now()

# Create Random Movie data

seeder = Seed.seeder()

seeder.add_entity(Movie, 100)
                  
def execute():
    seeder.execute()
    print("seeding completed")
    
    
    