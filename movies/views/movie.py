from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from requests import RequestException
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from movies.filters.movie import MovieFilter
from movies.models.movie import Movie
from movies.serializers.movie import MovieSerializer, MovieTopSerializer
from movies.utils import fetch_api_data


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = MovieFilter
    ordering_fields = ('title', 'year', 'imdbrating')

    serializers = {
        'default': MovieSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        title = request.data.get('title')

        if not title:
            return Response('Title is required.', status=status.HTTP_400_BAD_REQUEST)

        movie = Movie.objects.filter(title=title).first()

        if movie:
            serializer = self.get_serializer(movie)
            return Response(serializer.data, status=200)

        else:

            try:
                data = fetch_api_data(title, serializer)
            except RequestException:
                return Response('API service is unreachable.', status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except RuntimeError:
                return Response(f'Movie not found, {title}', status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response('Server cannot fetch valid data from the API',
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            serializer = self.get_serializer(data=data)

            if not serializer.is_valid():
                return Response('Server cannot fetch valid data from the API',
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            super(MovieViewSet, self).perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET'])
def top(request):
    movies = Movie.objects.filter(deleted=False).all()
    serializer = MovieTopSerializer(movies, many=True, context={'request': request})

    result = filter(lambda x: x['rank'] in range(4), serializer.data)

    return Response(result)
