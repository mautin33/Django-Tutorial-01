from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.utils import timezone

from random import randint

from django_seed import Seed

from helper.utils import Paginator, is_valid_uuid

from watchlist.models import (
    WatchList,
    StreamPlatform,
    Review
)
from watchlist.serializers import (
    WatchListSerializer,
    StreamPlatformSerializer,
    ReviewSerializer
)


class ReviewAV(APIView):
    serializer_class = ReviewSerializer
    
    def get_review(self, review_id):
                
        try:
            return Review.objects.filter(is_active=True).get(id=review_id)
        except Review.DoesNotExist:
            return None 

    
    def get_object(self, watch_list_id):
        try:
            return Review.objects.filter(is_active=True).filter(watch_list=watch_list_id)
        except Review.DoesNotExist:
            return None
        
        
    def get(self, request, *args, **kwargs):
        query_params = request.GET
        watch_list_id = query_params.get("id", False)
        validate_id = is_valid_uuid(watch_list_id) if watch_list_id else False

        if watch_list_id and validate_id:
            reviews_qs = self.get_object(watch_list_id)
            
            if reviews_qs is not None:
                serializer = self.serializer_class(instance=reviews_qs, many=True)
                data = {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                }
                return Response(data=data)
            data = {
                "data": [],
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)

        data = {
            "message": "No ID or Invalid ID!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)


    def post(self, request, *args, **kwargs):
        query_params = request.GET
        watch_list_id = query_params.get("id", False)
        validate_id = is_valid_uuid(watch_list_id) if watch_list_id else False
    
        if watch_list_id and validate_id:
          
            try:
                movie = WatchList.objects.get(id=watch_list_id)
            except WatchList.DoesNotExist:
                return None 
              
            if movie is not None: 
                serializer = self.serializer_class(data=request.data)

                if serializer.is_valid():
                    serializer.save(watch_list=movie)
                    data = {
                        "data": serializer.data,
                        "message": "Review Successfully Created!!!",
                        "status": status.HTTP_201_CREATED
                    }
                    return Response(data=data)
                data = {
                    "data": serializer.errors,
                    "message": "Failed To Create Review",
                    "status": status.HTTP_400_BAD_REQUEST
                }
                return Response(data=data)
            
            data = {
                "message": "Not Found",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)
        
        data = {
            "message": "No ID or Invalid ID!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)

    
    def put(self, request, *args, **kwargs):
        query_params = request.GET
        review_id = query_params.get("id", False)
        validate_review_id = is_valid_uuid(review_id) if review_id else False
        
        if review_id and validate_review_id:
            review = self.get_review(review_id)

            if review is not None:
                        
                serializer = self.serializer_class(instance=review, data=request.data)
                
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        "data": serializer.data,
                        "message": "Review Updated successfully!!!",
                        "status": status.HTTP_201_CREATED
                    }
                    return Response(data=data)
                data = {
                    "data": serializer.errors,
                    "message": "Failed to update Review!!!",
                    "status": status.HTTP_400_BAD_REQUEST
                }
 
            data = {
                "message": "Failed to Find Review!!!",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)
        
        data = {
            "message": "No Review ID or Invalid ID!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)    
          

    def delete(self, request, *args, **kwargs):
        query_params = request.GET
        review_id = query_params.get("id", False)
        validate_id = is_valid_uuid(review_id) if review_id else False

        if review_id and validate_id:
            
            try:
                review_qs = Review.objects.filter(is_active=True).get(id=review_id)
            except Review.DoesNotExist:
                return None 
                      
            if review_qs is not None:
                review_qs.soft_delete()
                data = {
                    "message": "Review Successfully Deleted!!!",
                    "status": status.HTTP_204_NO_CONTENT
                }
                return Response(data=data)
            data = {
                "message": "No Review Found!!!",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)
        data = {
            "message": "No ID or Invalid ID!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)
    

class StreamPlatformAV(APIView):
    serializer_class = StreamPlatformSerializer

    def get_object(self, id):
        try:
            return StreamPlatform.objects.get(id=id)
        except StreamPlatform.DoesNotExist:
            return None


    def get(self, request, *args, **kwargs):
        query_params = request.GET
        platform_id = query_params.get("id", False)
        validate_id = is_valid_uuid(platform_id) if platform_id else False

        if platform_id and validate_id:
            platform_qs = self.get_object(platform_id)
            if platform_qs is not None:
                serializer = self.serializer_class(instance=platform_qs)
                data = {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                }
                return Response(data=data)
            data = {
                "data": [],
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)

        platforms_qs = StreamPlatform.objects.all()
        if platforms_qs.exists():
            platforms = Paginator.paginate(
                request=request, queryset=platforms_qs)
            serializer = self.serializer_class(instance=platforms, many=True)
            data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "count": len(platforms)
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
            data = {
                "data": serializer.data,
                "message": "StreamPlatform created successfully!!!",
                "status": status.HTTP_201_CREATED
            }
            return Response(data=data)
        data = {
            "data": serializer.errors,
            "message": "Failed to create StreamPlatform!!!",
            "status": status.HTTP_400_BAD_REQUEST
        }
        return Response(data=data)


    def put(self, request, *args, **kwargs):
        query_params = request.GET
        platform_id = query_params.get("id", False)
        validate_id = is_valid_uuid(platform_id) if platform_id else False

        if platform_id and validate_id:
            platform_qs = self.get_object(platform_id)

            if platform_qs is not None:
                serializer = self.serializer_class(
                    instance=platform_qs, data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    data = {
                        "data": serializer.data,
                        "message": "StreamPlatform Successfully Updated!!!",
                        "status": status.HTTP_201_CREATED
                    }
                    return Response(data=data)
                data = {
                    "data": serializer.errors,
                    "message": "StreamPlatform Update Failed!!!",
                    "status": status.HTTP_400_BAD_REQUEST
                }
                return Response(data=data)

            data = {
                "message": "No StreamPlatform Found!!!",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)

        data = {
            "message": "No ID or Invalid ID!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)


    def delete(self, request, *args, **kwargs):
        query_params = request.GET
        platform_id = query_params.get("id", False)
        validate_id = is_valid_uuid(platform_id) if platform_id else False

        if platform_id and validate_id:
            platform_qs = self.get_object(platform_id)
            if platform_qs is not None:
                platform_qs.soft_delete()
                data = {
                    "message": "StreamPlatform Successfully Deleted!!!",
                    "status": status.HTTP_204_NO_CONTENT
                }
                return Response(data=data)
            data = {
                "message": "No StreamPlatform Found!!!",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)
        data = {
            "message": "No ID or Invalid ID!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)


class WatchListAV(APIView):
    serializer_class = WatchListSerializer

    def get_object(self, id):
        try:
            return WatchList.objects.filter(is_active=True).get(id=id)
        except WatchList.DoesNotExist:
            return None


    def get(self, request, *args, **kwargs):
        query_params = request.GET
        movie_id = query_params.get("id", False)
        validate_id = is_valid_uuid(movie_id) if movie_id else False

        if movie_id and validate_id:
            movie_qs = self.get_object(movie_id)

            if movie_qs is not None:
                serializer = self.serializer_class(instance=movie_qs)
                data = {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                }
                return Response(data=data)
            data = {
                "data": [],
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)

        movies_qs = WatchList.objects.filter(is_active=True).all()
        if movies_qs.exists():
            movies = Paginator.paginate(request=request, queryset=movies_qs)
            serializer = self.serializer_class(instance=movies, many=True)
            data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "count": len(movies)
            }
            return Response(data=data)
        data = {
            "data": [],
            "status": status.HTTP_200_OK,
            "count": 0
        }
        return Response(data=data)


    def post(self, request, *args, **kwargs):
        query_params = request.GET 
        platform_id = query_params.get("id", False)
        validate_id = is_valid_uuid(platform_id) if platform_id else False
    
        if platform_id and validate_id:
          
            try:
                platform = StreamPlatform.objects.filter(is_active=True).get(id=platform_id)
            except StreamPlatform.DoesNotExist:
                return None 
              
            if platform is not None: 
                serializer = self.serializer_class(data=request.data)

                if serializer.is_valid():
                    serializer.save(platform=platform)
                    data = {
                        "data": serializer.data,
                        "message": "Movie Successfully Created!!!",
                        "status": status.HTTP_201_CREATED
                    }
                    return Response(data=data)
                data = {
                    "data": serializer.errors,
                    "message": "Failed To Create Movie",
                    "status": status.HTTP_400_BAD_REQUEST
                }
                return Response(data=data)
            
            data = {
                "message": "Failed to Find Platform!!!",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)
        
        data = {
            "message": "No ID or Invalid ID!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)

        
    def put(self, request, *args, **kwargs):
        query_params = request.GET
        movie_id = query_params.get("id", False)
        validate_id = is_valid_uuid(movie_id) if movie_id else False

        if movie_id and validate_id:
            movie_qs = self.get_object(movie_id)
            
            if movie_qs is not None:
                serializer = self.serializer_class(instance=movie_qs, data=request.data)
                
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        "data": serializer.data,
                        "message": "Movie Successfully Updated!!!",
                        "status": status.HTTP_201_CREATED                       
                    }
                    return Response(data=data)
                data = {
                    "data": serializer.errors,
                    "message": "Movie Update Failed!!!",
                    "status": status.HTTP_400_BAD_REQUEST                
                }
                return Response(data=data)
            
        data = {
            "message": "No ID or Invalid ID!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)


    def delete(self, request, *args, **kwargs):
        query_params = request.GET
        movie_id = query_params.get("id", False)
        validate_id = is_valid_uuid(movie_id) if movie_id else False

        if movie_id and validate_id:
            movie_qs = self.get_object(movie_id)
            
            if movie_qs is not None:
                movie_qs.soft_delete()
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

        data = {
            "message": "No ID or Invalid ID!!!",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data=data)


# Create Dummy Streams data
now = timezone.now()

platforms = ("Netflix", "Amazon Prime Video", "ShowMax", "Youtube", "Vudu",
             "Apple TV+", "Disney +", "Starz", "Paramount +", "Amazon Hub Counter",)

def dump_platform():
    seeder = Seed.seeder()
    seeder.add_entity(StreamPlatform, 10, {
        "name": lambda x: platforms[randint(0, len(platforms) - 1)],
        "created_at": now,
        "updated_at": now
    })
    seeder.execute()
    print("seeding completed")


# Create Random Movie data
def dump_movies():
    platforms = StreamPlatform.objects.all()

    seeder = Seed.seeder()
    print(platforms.count(), "\n\n")

    seeder.add_entity(WatchList, 100, {
        "platform": lambda x: platforms[randint(0, platforms.count() - 1)],
        "created_at": now,
        "updated_at": now
    })
    seeder.execute()
    print("seeding completed")


# Create Review Movie data

random_no = (1,2,3,4,5,)

def dump_reviews():
    watch_lists = WatchList.objects.all()
    print(len(random_no),"\n\n")

    seeder = Seed.seeder()

    seeder.add_entity(Review, 100, {
        "watch_list": lambda x: watch_lists[randint(0, watch_lists.count() - 1)],
        "rating": lambda x: random_no[randint(1, len(random_no) - 1)],
        "created_at": now,
        "updated_at": now
    })
    seeder.execute()
    print("seeding completed")





