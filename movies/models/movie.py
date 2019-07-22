import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField(validators=[MinValueValidator(0, 'Year cannot be a negative value.')])
    rated = models.CharField(max_length=64, null=True)
    released = models.DateField(validators=[MaxValueValidator(datetime.datetime.now().date(),
                                                              'Release date cannot be greater that current date.')])
    runtime = models.CharField(max_length=64)
    genre = models.CharField(max_length=256)
    director = models.CharField(max_length=255, null=True)
    writer = models.CharField(max_length=512, null=True)
    actors = models.CharField(max_length=512, null=True)
    plot = models.TextField(null=True)
    language = models.CharField(max_length=256)
    country = models.CharField(max_length=128)
    awards = models.CharField(max_length=512, null=True)
    poster = models.URLField(null=True)
    metascore = models.IntegerField(validators=[MinValueValidator(0, 'Metascore cannot be a negative value.'),
                                                MaxValueValidator(100, 'Metascore cannot be greater than 100.')])
    imdbrating = models.FloatField(validators=[MinValueValidator(0, 'Rating cannot be a negative value.'),
                                               MaxValueValidator(10, 'Rating cannot be greater than 10.')])
    imdbvotes = models.CharField(max_length=24)
    imdbid = models.CharField(max_length=9)
    type = models.CharField(max_length=32)  # better make a choice field, but there is no info about all types
    dvd = models.DateField(validators=[MaxValueValidator(datetime.datetime.now().date(),
                                                         'DVD date cannot be greater than current date.')], null=True)
    boxoffice = models.CharField(max_length=24, null=True)
    production = models.CharField(max_length=255, null=True)
    website = models.URLField(null=True)

    deleted = models.BooleanField(default=False)

    def get_comments_count(self, request):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            return self.comments.filter(created__gte=start_date, created__lte=end_date).count()
        else:
            return self.comments.all().count()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
