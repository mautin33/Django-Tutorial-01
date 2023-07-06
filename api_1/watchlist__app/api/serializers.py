from rest_framework import serializers
from watchlist__app.models import Movie

        
class MovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = "__all__"              

    
        
        
        
        
    
        
        
       
       
        