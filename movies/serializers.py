from django.db.models import Avg
from rest_framework import serializers
from movies.models import Movie
from genres.serializers import GenreSerializer
from actors.serializers import ActorSerizalizer


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fiels = '__all__'

    def validate_release_date(self, value):
        if value.year < 1900:
            raise serializers.ValidationError('a data de lançamento não pode ser anterior a 1900.')
        return value

    def validate_resume(self, value):
        if len(value) > 500:
            raise serializers.ValidationError('Resumo não deve ser maior do que 500 caracteres. ')
        return value

    class MovieListDetailSerializer(serializers.ModelSerializer):
        actors = ActorSerizalizer(many=True)
        genre = GenreSerializer()
        rate = serializers.SerializerMethodField(read_only=True)

        class Meta:
            model = Movie
            fields = ['id', 'title', 'genre', 'actors', 'release_date', 'rate', 'resume']

        def get_rate(self, obj):
            rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']

            if rate:
                return round(rate, 1)
            return None

    class MovieStatsSerializer(serializers.Serializer):
        total_movies = serializers.IntegerField()
        movies_by_genre = serializers.ListField()
        total_reviews = serializers.IntegerField()
        average_starts = serializers.FloatField()
