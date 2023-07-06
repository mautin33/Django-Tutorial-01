from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from helper.utils import Paginator

from watchlist__app.models import Movie
from watchlist__app.api.serializers import MovieSerializer


class MovieList(APIView):
    serializer_class = MovieSerializer
    
    def get_object(self):
        try:
            return Movie.objects.all()
        except Movie.DoesNotExist:
            return None   
        
    def get(self, request, *args, **kwargs):
        movies_qs = self.get_object()
        if movies_qs is not None:
            movies = Paginator.paginate(request=request, queryset=movies_qs)
            serializer = self.serializer_class(instance=movies, many=True)
            data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "count": len(serializer.data)
            }
            return Response(data=data)
        data = {
            "data": [],
            "status": status.HTTP_200_OK,
            "count": 0
        }
        return Response(data=data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class MovieDetail(APIView):
    serializer_class = MovieSerializer
      
    def get_object(self, id):
        try:
            return Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return None         
        
    def get(self, request, id, *args, **kwargs):
        movie_qs = self.get_object(id)
        if movie_qs is not None:
            serializer = self.serializer_class(instance=movie_qs)
            data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK
            }
            return Response(data=data)
        data = {
            "data": [],
            "message": "No Movie Found!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)


    def put(self, request, id, *args, **kwargs):
        movie_qs = self.get_object(id)
        if movie_qs is not None:
            serializer = self.serializer_class(movie_qs, data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "data": serializer.data,
                    "message": "Movie Updated Successfully!!!",
                    "status": status.HTTP_204_NO_CONTENT
                }
                return Response(data=data)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = {
            "data": [],
            "message": "No Movie Found!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)
    
    
    def delete(self, request, id, *args, **kwargs):
        movie_qs = self.get_object(id)
        if movie_qs is not None:
            movie_qs.delete() 
            data = {
                "message": "Movie Deleted Successfully!!!",
                "status": status.HTTP_204_NO_CONTENT
            }
            return Response(data=data)
        data = {
            "data": [],
            "message": "No Movie Found!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)
    
