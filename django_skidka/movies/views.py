from typing import Any, Dict
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View


from .models import Movie, Category, Actor, Genre
from .forms import ReviewForm
from .models import Movie, Category, Actor, Genre, Rating, Reviews
from .forms import ReviewForm, RatingForm


class CategorySearch:
    """Фильтр поиска по категориям"""
    def get_categories(self):
        return Category.objects.all()

class GenreYear:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, CategorySearch, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 12
    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class MovieDetailView(GenreYear, CategorySearch, DetailView):
    """Полное описание фильма"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())



class FilterMoviesView(GenreYear, CategorySearch, ListView):
    """Фильтр фильмов"""
    paginate_by = 12
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre")) |
            Q(category__in=self.request.GET.getlist("category"))
        ).distinct()
        queryset = queryset.order_by('-id')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        return context

class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class Search(ListView):
    """Поиск"""
    paginate_by = 12
    # def get_queryset(self):
    #     return Movie.objects.filter(title__icontains=self.request.GET.get('q'))
    def get_queryset(self):
        q = self.request.GET.get('q').capitalize()
        return Movie.objects.filter(title__icontains=q)

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context
