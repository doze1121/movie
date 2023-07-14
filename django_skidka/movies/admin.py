from django.contrib import admin
from .models import Catagory, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews


admin.site.register(Catagory)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieShots)
admin.site.register(Actor)
admin.site.register(Rating)
admin.site.register(RatingStar)
admin.site.register(Reviews)
