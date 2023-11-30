from django.db import models
from datetime import date
from django.urls import reverse

class Category(models.Model):
    name = models.CharField('Категории', max_length=150)
    descriotion = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Actor(models.Model):
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'

class Genre(models.Model):
    name = models.CharField('Имя', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Movie(models.Model):
    title = models.CharField('Название', max_length=100)
    tagline = models.CharField('Слоган', max_length=100, default='', blank=True)
    description = models.TextField('Описание')
    # poster = models.ImageField('Постер', upload_to='movies/')
    poster = models.URLField('Ссылка на постер')
    year = models.PositiveSmallIntegerField('Дата выхода', default=2023)
    country = models.CharField('Страна', max_length=30, blank=True)
    directors = models.ManyToManyField(Actor, verbose_name='режиссер', related_name='film_director', blank=True) #ManyToMany отношение многих ко многим
    actros = models.ManyToManyField(Actor, verbose_name='актеры', related_name='film_actor', blank=True)
    genres = models.ManyToManyField(Genre, verbose_name='жанры', blank=True)
    world_premier = models.DateField('Премьера в мире', default=date.today, blank=True)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='указывать сумму в долларах', blank=True)
    fees_in_usa = models.PositiveIntegerField('Сборы в США', default=0, help_text='указывать сумму в долларах', blank=True)
    fees_in_world = models.PositiveIntegerField('Сборы в мире', default=0, help_text='указывать сумму в долларах', blank=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True) #ForeignKey отношение многих к одному
    #on_delete=models.SET_NULL данный аргумен указывает что будет происходить если мы удалим категорию и будет указывать null
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})
    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

class MovieShots(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE) #on_delete=models.CASCADE При удалении фильма удалятся все связанные кадры

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'

class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]

class Rating(models.Model):
    ip = models.CharField('IP адресс', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='фильм')

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
