from django_filters import rest_framework as filters

from movies.models.movie import Movie


class MovieFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')
    genre = filters.CharFilter(field_name='genre', lookup_expr='contains')
    writer = filters.CharFilter(field_name='writer', lookup_expr='contains')
    actors = filters.CharFilter(field_name='actors', lookup_expr='contains')
    language = filters.CharFilter(field_name='language', lookup_expr='contains')
    country = filters.CharFilter(field_name='country', lookup_expr='contains')

    class Meta:
        model = Movie
        fields = ['title', 'year', 'genre', 'writer', 'actors', 'language', 'country', 'type', 'deleted']
