from rest_framework import serializers

from movies.models.movie import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'rated', 'released', 'runtime', 'genre', 'director', 'writer', 'actors',
                  'plot', 'language', 'country', 'awards', 'poster', 'metascore', 'imdbrating', 'imdbvotes', 'imdbid',
                  'type', 'dvd', 'boxoffice', 'production', 'deleted')


class MovieTopSerializer(serializers.Serializer):
    movie_id = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    def get_movie_id(self, instance):
        return instance.id

    def get_total_comments(self, instance):
        return instance.get_comments_count(self.context['request'])

    def get_rank(self, instance):
        request = self.context['request']
        ranks = self._get_movies_ranks()

        return ranks[instance.get_comments_count(request)]

    def _get_movies_ranks(self):
        request = self.context['request']
        movies = Movie.objects.filter(deleted=False).all()

        comment_counts = sorted(list(set([i.get_comments_count(request) for i in movies])), reverse=True)
        ranks = {count: index + 1 for index, count in enumerate(comment_counts)}

        return ranks
